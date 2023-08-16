
document.addEventListener("DOMContentLoaded", function () {
  var formulario1 = document.getElementById("formulario1");
  var formulario2 = document.getElementById("formulario2");

  var radioOptions = document.getElementsByName("tipo_usuario");
  for (var i = 0; i < radioOptions.length; i++) {
      radioOptions[i].addEventListener("change", function () {
          if (this.value === "musico") {
              formulario1.style.display = "block";
              formulario2.style.display = "none";
          } else if (this.value === "grupo") {
              formulario1.style.display = "none";
              formulario2.style.display = "block";
          }
      });
  }
});
// Path: static\js\scripts.js
//FUNCIONES

document.addEventListener("DOMContentLoaded", function () {
  let currentIndex = 1; // Índice del usuario actual

  function showUser(index) {
      const usuarios = document.querySelectorAll(".usuario-card");
      usuarios.forEach((usuario) => {
          usuario.style.display = "none";
      });

      const usuarioActual = document.querySelector(`#usuario-${index}`);
      if (usuarioActual) {
          usuarioActual.style.display = "block";
      }
  }

  showUser(currentIndex);

  const btnLikes = document.querySelectorAll(".btn-like");
  const btnDislikes = document.querySelectorAll(".btn-dislike");

  btnLikes.forEach(btn => {
    btn.addEventListener("click", () => {
        const usuarioIdActual = btn.getAttribute("data-usuario-id");
        fetch(`/dar_like/${usuarioIdActual}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
        })
          .then(response => response.json())
          .then(data => {
              console.log("Like registrado:", data);
          })
          .catch(error => {
              console.error("Error al registrar el like:", error);
          });
          currentIndex++;
          showUser(currentIndex);
      });
  });

  btnDislikes.forEach(btn => {
    btn.addEventListener("click", () => {
        const usuarioIdActual = btn.getAttribute("data-usuario-id");
        fetch(`/dar_dislike/${usuarioIdActual}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
        })
          .then(response => response.json())
          .then(data => {
              console.log("Dislike registrado:", data);
          })
          .catch(error => {
              console.error("Error al registrar el dislike:", error);
          }); 
          currentIndex++;
          showUser(currentIndex);
      });
  });
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