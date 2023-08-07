
document.addEventListener("DOMContentLoaded", function () {
  var formulario1 = document.getElementById("formulario1");
  var formulario2 = document.getElementById("formulario2");

  var radioOptions = document.getElementsByName("inlineRadioOptions");
  for (var i = 0; i < radioOptions.length; i++) {
    radioOptions[i].addEventListener("change", function () {
      if (this.value === "option1") {
        formulario1.style.display = "block";
        formulario2.style.display = "none";
      } else if (this.value === "option2") {
        formulario1.style.display = "none";
        formulario2.style.display = "block";
      }
    });
  }
});



function mostrarFormulario() {
    var checkbox1 = document.getElementById('inlineRadio1');
    var checkbox2 = document.getElementById('inlineRadio2');
    var formulario1 = document.getElementById('formulario1');
    var formulario2 = document.getElementById('formulario2');

    if (checkbox1.checked) {
      formulario1.style.display = 'block';
    } else {
      formulario1.style.display = 'none';
    }

    if (checkbox2.checked) {
      formulario2.style.display = 'block';
    } else {
      formulario2.style.display = 'none';
    }
  }