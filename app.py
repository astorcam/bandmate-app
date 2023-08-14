from flask import Flask, render_template, request, redirect, url_for, flash
from db import db
from flask_bcrypt import Bcrypt
from bleach import  clean
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user


from models import Usuario, Musico, Grupo, Like, Dislike

app = Flask(__name__)
app.secret_key = 'CLAVE_SECRETA'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
bcrypt = Bcrypt(app)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:psswrd@localhost/bandmate'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Crear todas las tablas en la base de datos
with app.app_context():
    #db.drop_all()
    db.create_all()

# Rutas de la aplicación
@app.route('/')
def portada():
    return render_template('portada.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        contraseña_ingresada = request.form['contraseña']
        #verificacione de las credenciales
        user = Usuario.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.contraseña, contraseña_ingresada):
            login_user(user)
            return redirect(url_for('inicio'))
        else:
            flash('Nombre de usuario o contraseña incorrectos', 'error')
    
    return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/ayuda')
@login_required
def ayuda():
    return render_template('ayuda.html')

@app.route('/config')
def configuracion():
    return render_template('configuracionBanda.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        # Obtener los datos del formulario de registro
        nombre = clean(request.form['nombre'])
        email = clean(request.form['email'])
        contraseña = clean(request.form['contraseña'])
        direccion = clean(request.form['direccion'])
        genero_musical = clean(request.form['genero_musical'])
        tipo_usuario = clean(request.form['tipo_usuario'])
        busca_genero = clean(request.form['busca_genero'])
        
        # Verifica que todos los campos del formulario estén completados
        if not nombre or not email or not contraseña or not direccion or not genero_musical or not tipo_usuario or not busca_genero:
            flash('Por favor, completa todos los campos del formulario.', 'error')
            return redirect(url_for('registro'))
        
        # Verifica que el usuario no esté creado ya
        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            flash('El correo electrónico ya está registrado. Por favor, utiliza otro correo.', 'error')
            return redirect(url_for('registro'))
        
        hashed_password = bcrypt.generate_password_hash(contraseña).decode('utf-8')
        
        if tipo_usuario == 'musico':
            sexo = clean(request.form['sexo'])
            edad = clean(request.form['edad'])
            instrumento_principal = clean(request.form['instrumento_principal'])
            
            nuevo_usuario = Musico(
                tipo=tipo_usuario,
                nombre=nombre,
                email=email,
                contraseña=hashed_password,
                direccion=direccion,
                genero_musical=genero_musical,
                busca_genero=busca_genero,
                sexo=sexo,
                edad=edad,
                instrumento_principal=instrumento_principal
            )
        elif tipo_usuario == 'grupo':
            busca_instrumento = clean(request.form['busca_instrumento'])
            
            nuevo_usuario = Grupo(
                tipo=tipo_usuario,
                nombre=nombre,
                email=email,
                contraseña=hashed_password,
                direccion=direccion,
                genero_musical=genero_musical,
                busca_genero=busca_genero,
                busca_instrumento=busca_instrumento,
            )
        nuevo_usuario.save()
        flash('Registro exitoso', 'success')
        return redirect(url_for('login'))
    return render_template('registro.html')


""" @app.route('/inicio')
@login_required
def inicio():
    return render_template('home.html') """

@app.route('/inicio')
@login_required
def inicio():
    usuarios_cercanos = current_user.buscar_usuarios_cercanos(current_user) 
    likes = Like.query.filter_by(emisor_id=current_user.id).all()
    usuarios_con_like = [like.receptor_id for like in likes]

    dislikes = Dislike.query.filter_by(emisor_id=current_user.id).all()
    usuarios_con_dislike = [dislike.receptor_id for dislike in dislikes]

    # Filtrar los usuarios cercanos quitando los usuarios con like o dislike
    usuarios_cercanos = [usuario for usuario in usuarios_cercanos if usuario.id not in usuarios_con_like and usuario.id not in usuarios_con_dislike]

    if current_user.tipo=='musico':
        return render_template('home_musico.html', usuarios_cercanos=usuarios_cercanos)


#funciones
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

if __name__ == '__main__':
    app.run(debug=True)