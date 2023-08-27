from flask import Flask, render_template, request, redirect, url_for, flash,jsonify, session
from db import db
from flask_bcrypt import Bcrypt
from bleach import  clean
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
import os
import time
import re
import spotipy
from spotipy import Spotify, SpotifyOAuth, SpotifyClientCredentials



from models import Usuario, Musico, Grupo, Like, Dislike, Match, GoogleMapsAPI, Foto, Video, Audio, Mensaje, SpotifyAPI

app = Flask(__name__)
app.secret_key = 'CLAVE_SECRETA'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
bcrypt = Bcrypt(app)

#Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:psswrd@localhost/bandmate'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#Crear todas las tablas en la base de datos
with app.app_context():
    #db.drop_all()
    db.create_all()

#Rutas de la aplicación
@app.route('/')
def portada():
    return render_template('portada.html')

@app.route('/perfil_detallado/<int:usuario_id>')
@login_required
def perfil_detallado(usuario_id):
    usuario = Usuario.query.get(usuario_id)
    googlemaps=GoogleMapsAPI()
    ciudad = googlemaps.buscar_ciudad(usuario.direccion)
    fotos=Foto.query.filter_by(user_id=usuario.id).all()
    videos=Video.query.filter_by(user_id=usuario.id).all()
    audios=Audio.query.filter_by(user_id=usuario.id).all()
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
    if usuario.tipo == 'musico':
        musico = Musico.query.get(usuario_id)
        return render_template('perfil_musico.html', usuario=usuario, musico=musico, ciudad=ciudad, multimedia_list=multimedia_list)
    else:
        grupo = Grupo.query.get(usuario_id)
        return render_template('perfil_grupo.html', usuario=usuario, grupo=grupo, ciudad=ciudad, multimedia_list=multimedia_list)

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
    if usuario_actual.tipo == 'grupo':
        grupo_actual = Grupo.query.get(usuario_actual.id)
        return render_template('perfil_personal_grupo.html', usuario=usuario_actual, grupo=grupo_actual, ciudad=ciudad, multimedia_list=multimedia_list)
    
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
        
        multimedia_list.append({"tipo": "foto", "url": filename, "id": foto.id})
    for video in videos:
        filename = os.path.basename(video.video_url)
        multimedia_list.append({"tipo": "video", "url": filename, "id": video.id})
    for audio in audios:
        filename = os.path.basename(audio.audio_url)
        multimedia_list.append({"tipo": "audio", "url": filename, "id": audio.id})
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
        if usuario_actual.tipo=='grupo':
            grupo_actual = Grupo.query.get(usuario_actual.id)
            instrumentos=clean(request.form['instrumentos'])
            grupo_actual.instrumentos = instrumentos
            grupo_actual.save()            
            
        return redirect(url_for('perfil_personal'))
    
@app.route('/eliminar_foto/<int:multimedia_id>', methods=['POST'])
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
    return redirect(url_for('editar_perfil'))

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
        nombre = clean(request.form['nombre'])
        email = clean(request.form['email'])
        contraseña = clean(request.form['contraseña'])
        direccion = clean(request.form['direccion'])
        genero_musical = clean(request.form['genero_musical'])
        tipo_usuario = clean(request.form['tipo_usuario'])
        busca_genero = clean(request.form['busca_genero'])
        
        if not nombre or not email or not contraseña or not direccion or not genero_musical or not tipo_usuario or not busca_genero:
            flash('Por favor, completa todos los campos del formulario.', 'error')
            return redirect(url_for('registro'))
        
        if not validate_email(email):
            flash('El correo electrónico no cumple con el formato requerido. Por favor, utiliza otro correo.', 'error')
            return redirect(url_for('registro'))
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
    multimedia_list = []
    for usuario in usuarios_cercanos:
        fotos=Foto.query.filter_by(user_id=usuario.id).all()
        videos=Video.query.filter_by(user_id=usuario.id).all()
        audios=Audio.query.filter_by(user_id=usuario.id).all()
        for foto in fotos:
            filename = os.path.basename(foto.foto_url)
            multimedia_list.append({"tipo": "foto", "url": filename, "user_id": foto.user_id})
        for video in videos:
            filename = os.path.basename(video.video_url)
            multimedia_list.append({"tipo": "video", "url": filename, "user_id": video.user_id})
        for audio in audios:
            filename = os.path.basename(audio.audio_url)
            multimedia_list.append({"tipo": "audio", "url": filename, "user_id": audio.user_id})
    if current_user.tipo=='musico':
        return render_template('home_musico.html', usuarios_cercanos=usuarios_cercanos, multimedia_list=multimedia_list)
    elif current_user.tipo=='grupo':
        return render_template('home_grupo.html', usuarios_cercanos=usuarios_cercanos, multimedia_list=multimedia_list)
    
@app.route('/dar_like/<int:usuario_id>', methods=['GET', 'POST'])
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
            return jsonify({'message': 'Hubo match'})
            
        else:
            return jsonify({'message': 'No hubo match'})
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
    
@app.route('/match')
@login_required
def match():
    return render_template('match.html')
    
@app.route('/matches')
@login_required
def matches():
    if current_user.tipo == 'musico':
        matches = Match.query.filter_by(musico_id=current_user.id).all()
        usuarios_match=[]
        multimedia_list=[]
        for match in matches:
            usuarios_match.append(Usuario.query.get(match.grupo_id))
        print(usuarios_match)
        for usuario in usuarios_match:
            foto=Foto.query.filter_by(user_id=usuario.id).first()
            if foto:
                filename = os.path.basename(foto.foto_url)
                multimedia_list.append({"url": filename, "user_id": foto.user_id})
    else:
        matches = Match.query.filter_by(grupo_id=current_user.id).all()
        usuarios_match=[]
        multimedia_list=[]
        for match in matches:
            usuarios_match.append(Usuario.query.get(match.musico_id))
        for usuario in usuarios_match:
            foto=Foto.query.filter_by(user_id=usuario.id).first()
            if foto:
                filename = os.path.basename(foto.foto_url)
                multimedia_list.append({"url": filename, "user_id": foto.user_id})
    return render_template('listaChats.html', usuarios_match=usuarios_match, multimedia_list=multimedia_list)
    
@app.route('/chat/<int:usuario_id>')
@login_required
def chat(usuario_id):
    usuario_actual = current_user
    usuario = Usuario.query.get(usuario_id)
    mensajes = Mensaje.query.filter_by(emisor_id=usuario_actual.id, receptor_id=usuario_id).order_by(Mensaje.fecha.asc()).all()
    mensajes.extend(Mensaje.query.filter_by(emisor_id=usuario_id, receptor_id=usuario_actual.id).order_by(Mensaje.fecha.asc()).all())
    mensajes.sort(key=lambda mensaje: mensaje.fecha)
    filename = ""
    foto=Foto.query.filter_by(user_id=usuario.id).first()
    if foto:
        filename = os.path.basename(foto.foto_url)
    return render_template('chat.html', usuario=usuario, mensajes=mensajes, filename=filename)
 
@app.route('/enviar_mensaje/<int:usuario_id>', methods=['POST'])
@login_required
def enviar_mensaje(usuario_id):
    usuario_actual = current_user
    texto = clean(request.form['texto'])
    mensaje = Mensaje(emisor_id=usuario_actual.id, receptor_id=usuario_id, texto=texto)
    mensaje.save()
    return redirect(url_for('chat', usuario_id=usuario_id))   

@app.route('/SpotifyAuth')
@login_required
def spotify_auth():
    sp_oauth=SpotifyAPI().create_Spotify_OAuth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route("/callback")
def callback():
    sp_oauth=SpotifyAPI().create_Spotify_OAuth()
    token_info=sp_oauth.get_access_token(request.args["code"])
    session["token_info"] = token_info
    return redirect(url_for("get_cancion_fav"))

@app.route("/get_cancion_fav")
@login_required
def get_cancion_fav():
    token_info=get_token()
    sp=spotipy.Spotify(auth=token_info['access_token'])
    results=sp.current_user_saved_tracks(limit=1)
    items = results['items']   
    nombre_cancion =items[0]['track']['name']
    current_user.cancion_fav = nombre_cancion
    track_id=items[0]['track']['id']
    track_info=sp.track(track_id)
    preview_url = track_info['preview_url']
    current_user.cancion_url = preview_url
    current_user.save()
    return redirect(url_for("editar_perfil"))

#funciones
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

def get_token():
    token_info=session.get("token_info", None)
    if not token_info:
        raise "Exception"
    now=time.time()
    is_expired=token_info["expires_at"]-now<60
    refresh_token=token_info["refresh_token"]
    if is_expired:
        sp_oauth=SpotifyAPI().create_Spotify_OAuth()
        token_info=sp_oauth.refresh_access_token(refresh_token)
    return token_info

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)


if __name__ == '__main__':
    app.run(debug=True)