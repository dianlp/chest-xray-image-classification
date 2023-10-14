import base64
import os
from flask import Flask, render_template, request
from io import BytesIO
from keras.models import load_model
from keras.utils import image_utils
from PIL import Image
import cv2
import numpy as np

model = load_model('model_86%.h5')
model.make_predict_function()

app = Flask(__name__)

@app.route('/home')
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/deteksi')
def deteksi():
    return render_template('analisis.html')

def predict_label(img):
    i = image_utils.img_to_array(img)/255.0
    i = i.reshape(1, 224, 224, 3)

    prob = model.predict(i)
    labels = "TBC" if prob[0][0] >= 0.5 else "Normal"
    classified_prob = prob[0][0] if prob[0][0] >= 0.5 else 1 - prob[0][0]

    return labels, classified_prob

def preprocess(img):
    i = np.asarray(img)
    rgb_pic = cv2.cvtColor(i, cv2.COLOR_BGR2RGB)
    gray_pic = cv2.cvtColor(rgb_pic, cv2.COLOR_BGR2GRAY)
    pic_eqhist = cv2.equalizeHist(gray_pic)
    im = Image.fromarray(np.uint8(pic_eqhist))
    return im

@app.route('/hasil_deteksi', methods=['POST'])
def prediksi():
    if request.method == 'POST':
        img = request.files['my_image']
        img_path = (os.path.join('static/', img.filename))
        img.save(img_path)

        i = cv2.imread(img_path)
        pic = preprocess(i)
        pic = pic.convert('RGB')
        pic = pic.resize((224, 224), Image.NEAREST)
        buffered = BytesIO()
        pic.save(buffered, format="JPEG")
        im = base64.b64encode(buffered.getvalue()).decode('ascii')

        predict, prob = predict_label(pic)
        prob = round((prob * 100), 2)
        
    return render_template("hasil-analisis.html", predict=predict, prob=prob, img_path = img.filename, eqhist=im)

@app.route('/hasil_deteksi/<img>')
def analis(img):
    img_path = (os.path.join('static/', img))
    i = cv2.imread(img_path)
    pic = preprocess(i)
    pic = pic.convert('RGB')
    pic = pic.resize((224, 224), Image.NEAREST)
    buffered = BytesIO()
    pic.save(buffered, format="JPEG")
    im = base64.b64encode(buffered.getvalue()).decode('ascii')

    predict, prob = predict_label(pic)
    prob = round((prob * 100), 2)

    return render_template('hasil-analisis.html', prediction=predict, prob=prob, pic=img, eqhist=im)

@app.route('/upload-lagi', methods=['GET', 'POST'])
def ulang():
    if request.method == 'POST':
        file = request.form.get('gambar')
        i = (os.path.join('static/', file))
        os.remove(i)
    return render_template('analisis.html')

if __name__ == '__main__':
    app.debug = True
    app.run()