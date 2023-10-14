$(document).on('change', '.custom-file-input', function () {


  var filesCount = $(this)[0].files.length;

  var textbox = $(this).next('.custom-file-label');

  if (filesCount === 1) {
    var fileName = $(this).val().split('\\').pop();
    textbox.text(fileName);
  } else {
    textbox.text(filesCount + ' files selected');
  }



  if (typeof (FileReader) != "undefined") {
    var dvPreview = $("#divImageMediaPreview");
    dvPreview.html("");
    $($(this)[0].files).each(function () {
      var file = $(this);
      var reader = new FileReader();
      reader.onload = function (e) {
        var img = $("<img />");
        img.attr("style", "width: 350px; height:350px; padding: 10px;");
        img.attr("src", e.target.result);
        dvPreview.append(img);
      }
      reader.readAsDataURL(file[0]);
    });
  } else {
    alert("This browser does not support HTML5 FileReader.");
  }


});