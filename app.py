from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:psswrd@localhost/bandmate'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)
# Crear todas las tablas en la base de datos
with app.app_context():
    db.create_all()

# Rutas de la aplicación
@app.route('/')
def portada():
    return render_template('portada.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/ayuda')
def ayuda():
    return render_template('ayuda.html')

@app.route('/config')
def configuracion():
    return render_template('configuracionBanda.html')

""" @app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
         # Obtener los datos del formulario de registro
        nombre = request.form['nombre']
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        direccion = request.form['direccion']
        genero_musical = request.form['genero_musical']
        tipo_usuario = request.form['tipo_usuario']
        
           # Verifica que todos los campos del formulario estén completados
        if not nombre or not correo or not contraseña or not direccion or not genero_musical or not tipo_usuario:
            flash('Por favor, completa todos los campos del formulario.', 'error')
            return redirect(url_for('registro'))
        
            # Verifica que el usuario no este creado ya
        usuario_existente = Usuario.query.filter_by(correo=correo).first()
        if usuario_existente:
            flash('El correo electrónico ya está registrado. Por favor, utiliza otro correo.', 'error')
            return redirect(url_for('registro'))
              
        flash('Registro exitoso', 'success')
        return redirect(url_for('login'))
    return render_template('registro.html') """

if __name__ == '__main__':
    app.run(debug=True)