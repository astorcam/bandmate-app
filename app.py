from flask import Flask, render_template, request, redirect, url_for, flash
from db import db
from models import Usuario, Musico, Grupo

app = Flask(__name__)
app.secret_key = 'CLAVE_SECRETA'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:psswrd@localhost/bandmate'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db.init_app(app)
# Crear todas las tablas en la base de datos
with app.app_context():
    db.drop_all()
    db.create_all()

# Rutas de la aplicación
@app.route('/')
def portada():
    return render_template('portada.html')

@app.route('/login')
def login():
    return render_template('login.html')

""" @app.route('/registro')
def registro():
    return render_template('registro.html') """

@app.route('/ayuda')
def ayuda():
    return render_template('ayuda.html')

@app.route('/config')
def configuracion():
    return render_template('configuracionBanda.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
         # Obtener los datos del formulario de registro
        nombre = request.form['nombre']
        email = request.form['email']
        contraseña = request.form['contraseña']
        direccion = request.form['direccion']
        genero_musical = request.form['genero_musical']
        tipo_usuario = request.form['tipo_usuario']
        busca_genero = request.form['busca_genero']
        
           # Verifica que todos los campos del formulario estén completados
        if not nombre or not email or not contraseña or not direccion or not genero_musical or not tipo_usuario or not busca_genero:
            flash('Por favor, completa todos los campos del formulario.', 'error')
            return redirect(url_for('registro'))
        
            # Verifica que el usuario no este creado ya
        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            flash('El correo electrónico ya está registrado. Por favor, utiliza otro correo.', 'error')
            return redirect(url_for('registro'))
        
        # Registra al usuario
        if tipo_usuario == 'musico':
            sexo = request.form['sexo']
            edad = request.form['edad']
            instrumento_principal = request.form['instrumento_principal']
            
            nuevo_usuario = Musico(
                tipo=tipo_usuario,
                nombre=nombre,
                email=email,
                contraseña=contraseña,
                direccion=direccion,
                genero_musical=genero_musical,
                busca_genero=busca_genero,
                sexo=sexo,
                edad=edad,
                instrumento_principal=instrumento_principal
            )
        elif tipo_usuario == 'grupo':
            busca_instrumento = request.form['busca_instrumento']
            instrumentos = request.form['instrumentos']
            
            nuevo_usuario = Grupo(
                tipo=tipo_usuario,
                nombre=nombre,
                email=email,
                contraseña=contraseña,
                direccion=direccion,
                genero_musical=genero_musical,
                busca_genero=busca_genero,
                busca_instrumento=busca_instrumento,
                instrumentos=instrumentos
            )
        nuevo_usuario.save()
        flash('Registro exitoso', 'success')
        return redirect(url_for('login'))
    return render_template('registro.html')

if __name__ == '__main__':
    app.run(debug=True)