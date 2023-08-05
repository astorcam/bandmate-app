function mostrarFormulario() {
    var checkbox1 = document.getElementById('checkbox1');
    var checkbox2 = document.getElementById('checkbox2');
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