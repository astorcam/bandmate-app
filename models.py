from db import db
from datetime import datetime
import googlemaps
import requests

API_KEY='AIzaSyBgPGO5aDpDxfjFD5W_69CWy2b0dJXgolw'


class Usuario(db.Model):
    __tablename__ = 'usuario'

    id = db.Column('ID', db.Integer, primary_key=True, autoincrement=True)
    tipo = db.Column('TIPO', db.String(6), nullable=False)
    nombre = db.Column('NOMBRE', db.String(255), nullable=False)
    email = db.Column('EMAIL', db.String(255), nullable=False)
    contraseña = db.Column('CONTRASEÑA', db.String(255), nullable=False)
    direccion = db.Column('DIRECCION', db.String(255), nullable=False)
    cancion_fav = db.Column('CANCION_FAV', db.String(255))
    genero_musical = db.Column('GENERO_MUSICAL', db.String(255), nullable=False)
    descripcion = db.Column('DESCRIPCION', db.String(255))
    busca_genero = db.Column('BUSCA_GENERO', db.String(255), nullable=False)
    busca_distancia = db.Column('BUSCA_DISTANCIA', db.Integer)
    longitud = db.Column('LONGITUD', db.Float)
    latitud = db.Column('LATITUD', db.Float)
    
    def __init__(self, tipo, nombre, email, contraseña, direccion, genero_musical, busca_genero,  ):
        self.tipo = tipo
        self.nombre = nombre
        self.email = email
        self.contraseña = contraseña
        self.direccion = direccion
        self.genero_musical = genero_musical
        self.cancion_fav = None
        self.descripcion=None
        self.busca_genero = busca_genero
        self.busca_distancia = None
        # Llamada a la función para buscar latitud y longitud
        google_maps_api = GoogleMapsAPI()
        location= google_maps_api.buscar_latitud_longitud(direccion)
        self.latitud=location['lat']
        self.longitud=location['lng']
        
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
class Audio(db.Model):
    __tablename__ = 'audio'

    audio_id = db.Column('AUDIO_ID', db.Integer, primary_key=True)
    user_id = db.Column('USER_ID', db.Integer, db.ForeignKey('usuario.ID'), nullable=False)
    audio_url = db.Column('AUDIO_URL', db.String(255))

    usuario = db.relationship('Usuario', backref=db.backref('audios', lazy=True))

class Foto(db.Model):
    __tablename__ = 'foto'

    foto_id = db.Column('FOTO_ID', db.Integer, primary_key=True)
    user_id = db.Column('USER_ID', db.Integer, db.ForeignKey('usuario.ID'), nullable=False)
    foto_url = db.Column('FOTO_URL', db.String(255))

    usuario = db.relationship('Usuario', backref=db.backref('fotos', lazy=True))

class Video(db.Model):
    __tablename__ = 'video'

    video_id = db.Column('VIDEO_ID', db.Integer, primary_key=True)
    user_id = db.Column('USER_ID', db.Integer, db.ForeignKey('usuario.ID'), nullable=False)
    video_url = db.Column('VIDEO_URL', db.String(255))

    usuario = db.relationship('Usuario', backref=db.backref('videos', lazy=True))

    
class Musico(Usuario):
    __tablename__ = 'musico'

    id = db.Column(db.Integer, db.ForeignKey('usuario.ID'), primary_key=True)
    instrumento_principal = db.Column(db.String(255), nullable=False)
    sexo = db.Column(db.String(255), nullable=False)
    edad = db.Column(db.Integer, nullable=False)

    def __init__(self, tipo, nombre, email, contraseña, direccion, genero_musical, busca_genero,
                 instrumento_principal, sexo, edad):
        super().__init__(tipo, nombre, email, contraseña, direccion, genero_musical, busca_genero)
        self.instrumento_principal = instrumento_principal
        self.sexo = sexo
        self.edad = edad

class Grupo(Usuario):
    __tablename__ = 'grupo'

    id = db.Column(db.Integer, db.ForeignKey('usuario.ID'), primary_key=True)
    busca_instrumento = db.Column(db.String(255), nullable=True)
    instrumentos = db.Column(db.String(255), nullable=True)

    def __init__(self, tipo, nombre, email, contraseña, direccion, genero_musical, busca_genero,
                 busca_instrumento, instrumentos):
        super().__init__(tipo, nombre, email, contraseña, direccion, genero_musical, busca_genero)
        self.busca_instrumento = busca_instrumento
        self.instrumentos = instrumentos

# Clase Match
class Match(db.Model):
    __tablename__ = 'match_table'

    match_id = db.Column(db.Integer, primary_key=True)
    musico_id = db.Column(db.Integer, db.ForeignKey('musico.id'), nullable=False)
    grupo_id = db.Column(db.Integer, db.ForeignKey('grupo.id'), nullable=False)



# Clase Mensaje
class Mensaje(db.Model):
    __tablename__ = 'mensaje'

    mensaje_id = db.Column(db.Integer, primary_key=True)
    emisor_id = db.Column(db.Integer, db.ForeignKey('usuario.ID'), nullable=False)
    receptor_id = db.Column(db.Integer, db.ForeignKey('usuario.ID'), nullable=False)
    texto = db.Column(db.String(255), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
class Like(db.Model):
    __tablename__ = 'like_table'

    like_id = db.Column(db.Integer, primary_key=True)
    emisor_id = db.Column(db.Integer, db.ForeignKey('usuario.ID'), nullable=False)
    receptor_id = db.Column(db.Integer, db.ForeignKey('usuario.ID'), nullable=False)

class Dislike(db.Model):
    __tablename__ = 'dislike_table'

    dislike_id = db.Column(db.Integer, primary_key=True)
    emisor_id = db.Column(db.Integer, db.ForeignKey('usuario.ID'), nullable=False)
    receptor_id = db.Column(db.Integer, db.ForeignKey('usuario.ID'), nullable=False)

class GoogleMapsAPI:    
    def __init__(self, API_KEY='AIzaSyAO-2U9g7LQ0fHvkI4IfDBL_adMQflkcV4'):
        self.client = googlemaps.Client(key=API_KEY)
    
    def buscar_latitud_longitud(self, direccion):
        #llamada a la API de Google Maps
        API_KEY='AIzaSyAO-2U9g7LQ0fHvkI4IfDBL_adMQflkcV4'
        params = {
        'key': API_KEY,
        'address': direccion}

        url = 'https://maps.googleapis.com/maps/api/geocode/json?'
        response = requests.get(url, params=params).json()
        response.keys()
        print('ha llegado aqui 1')
        if response['status'] == 'OK' and 'results' in response: 
            location = response['results'][0]['geometry']['location']
            return location
        return None