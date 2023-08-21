from flask import Flask, render_template, request, redirect, url_for, flash,jsonify
from db import db
from flask_bcrypt import Bcrypt
from bleach import  clean
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
import os


from models import Usuario, Musico, Grupo, Like, Dislike, Match, GoogleMapsAPI, Foto, Video, Audio

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

@app.route('/perfil_detallado/<int:usuario_id>')
@login_required
def perfil_detallado(usuario_id):
    usuario = Usuario.query.get(usuario_id)
    googlemaps=GoogleMapsAPI()
    ciudad = googlemaps.buscar_ciudad(usuario.direccion)
    if usuario.tipo == 'musico':
        musico = Musico.query.get(usuario_id)
        return render_template('perfil_musico.html', usuario=usuario, musico=musico, ciudad=ciudad)
    else:
        grupo = Grupo.query.get(usuario_id)
        return render_template('perfil_grupo.html', usuario=usuario, grupo=grupo, ciudad=ciudad)

@app.route('/perfil_personal')
def perfil_personal():
    usuario_actual = current_user
    googlemaps=GoogleMapsAPI()
    ciudad = googlemaps.buscar_ciudad(usuario_actual.direccion)
    fotos=Foto.query.filter_by(user_id=usuario_actual.id).all()
    videos=Video.query.filter_by(user_id=usuario_actual.id).all()
    audios=Audio.query.filter_by(user_id=usuario_actual.id).all()
    multimedia_list = []
    for foto in fotos:
        filename = os.path.basename(foto.foto_url)
        
        multimedia_list.append({"tipo": "foto", "url": filename})
    for video in videos:
        filename = os.path.basename(video.video_url)
        multimedia_list.append({"tipo": "video", "url": filename})
    for audio in audios:
        filename = os.path.basename(audio.audio_url)
        multimedia_list.append({"tipo": "audio", "url": filename})
    if usuario_actual.tipo == 'musico':
        musico_actual = Musico.query.get(usuario_actual.id)
        return render_template('perfil_personal_musico.html', usuario=usuario_actual, musico=musico_actual, ciudad=ciudad, multimedia_list=multimedia_list)
    
@app.route('/editar_perfil')
def editar_perfil():
    usuario_actual = current_user
    googlemaps=GoogleMapsAPI()
    ciudad = googlemaps.buscar_ciudad(usuario_actual.direccion)
    fotos=Foto.query.filter_by(user_id=usuario_actual.id).all()
    videos=Video.query.filter_by(user_id=usuario_actual.id).all()
    audios=Audio.query.filter_by(user_id=usuario_actual.id).all()
    multimedia_list = []
    for foto in fotos:
        filename = os.path.basename(foto.foto_url)
        
        multimedia_list.append({"tipo": "foto", "url": filename})
    for video in videos:
        filename = os.path.basename(video.video_url)
        multimedia_list.append({"tipo": "video", "url": filename})
    for audio in audios:
        filename = os.path.basename(audio.audio_url)
        multimedia_list.append({"tipo": "audio", "url": filename})
    if usuario_actual.tipo == 'musico':
        musico_actual = Musico.query.get(usuario_actual.id)
        return render_template('editar_perfil_musico.html', usuario=usuario_actual, musico=musico_actual, ciudad=ciudad, multimedia_list=multimedia_list)
    else:
        grupo_actual = Grupo.query.get(usuario_actual.id)
        return render_template('editar_perfil_grupo.html', usuario=usuario_actual, grupo=grupo_actual,  ciudad=ciudad,  multimedia_list=multimedia_list)
    
@app.route('/guardar_cambios_perfil', methods=['GET', 'POST'])
def guardar_cambios_perfil():
    usuario_actual = current_user
    if request.method == 'POST':
        genero_musical = clean(request.form['genero_musical'])
        descripcion = clean(request.form['descripcion'])
        if genero_musical != "Elige...":
            usuario_actual.genero_musical = genero_musical
        usuario_actual.descripcion = descripcion
        usuario_actual.save()
        
        if 'foto' in request.files:
            foto = request.files['foto']
            if foto.filename:
                foto.save(os.path.join('static/uploads', foto.filename))
                foto_url = os.path.join('static/uploads', foto.filename)
                nueva_foto = Foto(user_id=usuario_actual.id, foto_url=foto_url)
                nueva_foto.save()

        if 'audio' in request.files:
            audio = request.files['audio']
            if audio.filename:
                audio.save(os.path.join('static/uploads', audio.filename))
                audio_url = os.path.join('static/uploads', audio.filename)
                nuevo_audio = Audio(user_id=usuario_actual.id, audio_url=audio_url)
                nuevo_audio.save()

        if 'video' in request.files:
            video = request.files['video']
            if video.filename:
                video.save(os.path.join('static/uploads', video.filename))
                video_url = os.path.join('static/uploads', video.filename)
                nuevo_video = Video(user_id=usuario_actual.id, video_url=video_url)
                nuevo_video.save()

        usuario_actual.save()
        return redirect(url_for('perfil_personal'))
    
""" @app.route('/eliminar_foto/<int:multimedia_id>', methods=['POST'])
def eliminar_foto(multimedia_id):
    foto = Foto.query.get(multimedia_id)
    if foto:
        foto.delete()
    return redirect(url_for('editar_perfil'))

@app.route('/eliminar_audio/<int:multimedia_id>', methods=['POST'])
def eliminar_audio(multimedia_id):
    audio = Audio.query.get(multimedia_id)
    if audio:
        audio.delete()
    return redirect(url_for('editar_perfil'))

@app.route('/eliminar_video/<int:multimedia_id>', methods=['POST'])
def eliminar_video(multimedia_id):
    video = Video.query.get(multimedia_id)
    if video:
        video.delete()
    return redirect(url_for('editar_perfil')) """

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
    usuario_actual = current_user
    if usuario_actual.tipo == 'musico':
        musico_actual = Musico.query.get(usuario_actual.id)
        return render_template('configuracionMusico.html', usuario=usuario_actual, musico=musico_actual)
    else:
        grupo_actual = Grupo.query.get(usuario_actual.id)
        return render_template('configuracionGrupo.html', usuario=usuario_actual, grupo=grupo_actual)     
    
@app.route('/actualizar_datos', methods=['GET', 'POST'])
@login_required
def actualizar_datos():
    usuario_actual = current_user
    if request.method == 'POST':
            nombre = clean(request.form['nombre'])
            email = clean(request.form['email'])
            direccion = clean(request.form['direccion'])
            if not nombre or not email or not direccion:
                flash('Por favor, completa todos los campos del formulario.', 'error')
                return redirect(url_for('configuracion')) 
            usuario_existente = Usuario.query.filter_by(email=email).first()
            if usuario_existente and usuario_existente.id != usuario_actual.id:
                flash('El correo electrónico ya está registrado. Por favor, utiliza otro correo.', 'error')
                return redirect(url_for('configuracion'))    
            google_maps_api = GoogleMapsAPI()
            location= google_maps_api.buscar_latitud_longitud(direccion)
            usuario_actual.latitud=location['lat']
            usuario_actual.longitud=location['lng']      
            usuario_actual.nombre = nombre
            usuario_actual.email = email
            usuario_actual.direccion = direccion
            usuario_actual.save()
            if usuario_actual.tipo == 'musico':
                musico_actual = Musico.query.get(usuario_actual.id)   
                instrumento_principal = clean(request.form['instrumento_principal'])
                if instrumento_principal!="Elige...":
                    musico_actual.instrumento_principal = instrumento_principal
                    musico_actual.save()
            flash('Datos actualizados', 'success')
            return redirect(url_for('configuracion'))

        
@app.route('/actualizar_busqueda', methods=['GET', 'POST']) 
@login_required
def actualizar_busqueda():
    usuario_actual=current_user
    if request.method == 'POST':
        busca_distancia = clean(request.form['busca_distancia'])
        busca_genero = clean(request.form['busca_genero'])
        if not busca_distancia or not busca_genero:
                flash('Por favor, completa todos los campos del formulario.', 'error')
                return redirect(url_for('configuracion')) 
        usuario_actual.busca_distancia = busca_distancia
        if busca_genero!="Elige...":
                usuario_actual.busca_genero = busca_genero
        usuario_actual.save()
        if usuario_actual.tipo == 'grupo':
            grupo_actual = Grupo.query.get(usuario_actual.id)
            busca_instrumento = clean(request.form['busca_instrumento'])
            if busca_instrumento!="Elige...":
                grupo_actual.busca_instrumento = busca_instrumento
                grupo_actual.save()
        flash('Datos actualizados', 'success')
        return redirect(url_for('configuracion'))
    
@app.route('/actualizar_contraseña', methods=['GET', 'POST'])
@login_required
def actualizar_contraseña():
    usuario_actual = current_user
    if request.method == 'POST':
        contraseña_actual = request.form['contraseña_actual']
        contraseña_nueva = request.form['contraseña_nueva']
        contraseña_nueva2 = request.form['contraseña_nueva2']
        if not contraseña_actual or not contraseña_nueva or not contraseña_nueva2:
            flash('Por favor, completa todos los campos del formulario.', 'error')
            return redirect(url_for('configuracion'))
        if not bcrypt.check_password_hash(usuario_actual.contraseña, contraseña_actual):
            flash('La contraseña actual no es correcta.', 'error')
            return redirect(url_for('configuracion'))
        if contraseña_nueva != contraseña_nueva2:
            flash('Las contraseñas nuevas no coinciden.', 'error')
            return redirect(url_for('configuracion'))
        usuario_actual.contraseña = bcrypt.generate_password_hash(contraseña_nueva).decode('utf-8')
        usuario_actual.save()
        flash('Contraseña actualizada', 'success')
        return redirect(url_for('configuracion'))
    
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
    elif current_user.tipo=='grupo':
        return render_template('home_grupo.html', usuarios_cercanos=usuarios_cercanos)
    
@app.route('/dar_like/<int:usuario_id>', methods=['POST'])
@login_required
def dar_like(usuario_id):
    usuario = Usuario.query.get(usuario_id)
    if usuario:
        like = Like(emisor=current_user, receptor=usuario)
        like.save()
        match = None
        if Like.query.filter_by(emisor_id=usuario_id, receptor_id=current_user.id).first():
            if current_user.tipo == 'musico':
                match = Match(musico_id=current_user.id, grupo_id=usuario_id)
            else:
                match = Match(musico_id=usuario_id, grupo_id=current_user.id)
            match.save()            
    return jsonify({'message': 'Operación completada'})


@app.route('/dar_dislike/<int:usuario_id>', methods=['POST'])
@login_required
def dar_dislike(usuario_id):
    usuario = Usuario.query.get(usuario_id)
    if usuario:
        dislike = Dislike(emisor=current_user, receptor=usuario)
        dislike.save()
    else:
        return 404

#funciones
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

if __name__ == '__main__':
    app.run(debug=True)