from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from db import db
from datetime import datetime
import googlemaps
import requests
from math import radians, sin, cos, sqrt, atan2


API_KEY='AIzaSyBgPGO5aDpDxfjFD5W_69CWy2b0dJXgolw'


class Usuario(db.Model, UserMixin):
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
        self.busca_distancia = 50 # Por defecto 50 km
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
    
        

    @classmethod
    def buscar_usuarios_cercanos(cls, self):
        usuarios_cercanos_temp = []
        if self.tipo == 'musico':
            grupos_cercanos = Grupo.query.filter_by(genero_musical=self.busca_genero).all()
            usuarios_cercanos_temp.extend(grupos_cercanos)
        elif self.tipo == 'grupo':
            musicos_cercanos = Musico.query.filter_by(genero_musical=self.busca_genero).all()
            usuarios_cercanos_temp.extend(musicos_cercanos)
        usuarios_cercanos_temp = [usuario for usuario in usuarios_cercanos_temp if usuario != self]
        usuarios_cercanos_temp = [usuario for usuario in usuarios_cercanos_temp if usuario.calcular_distancia(usuario.latitud, usuario.longitud, self.latitud, self.longitud) <= self.busca_distancia]
        
        if self.tipo == 'grupo':
            user_grupo = Grupo.query.filter_by(id=self.id).first()
            usuarios_cercanos_temp = [usuario for usuario in usuarios_cercanos_temp if usuario.instrumento_principal == user_grupo.busca_instrumento]

        return usuarios_cercanos_temp

    @classmethod
    def calcular_distancia(self, latitud1, longitud1, latitud2, longitud2):
           # Radio de la Tierra en kilómetros
        radio_tierra = 6371.0

        # Convertir las coordenadas de latitud y longitud a radianes
        latitud1 = radians(latitud1)
        longitud1 = radians(longitud1)
        latitud2 = radians(latitud2)
        longitud2 = radians(longitud2)

        # Diferencias de latitud y longitud
        delta_latitud = latitud2 - latitud1
        delta_longitud = longitud2 - longitud1

        # Fórmula de Haversine para calcular la distancia entre dos puntos en una esfera
        a = sin(delta_latitud / 2)**2 + cos(latitud1) * cos(latitud2) * sin(delta_longitud / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distancia = radio_tierra * c

        return distancia
    
class Audio(db.Model):
    __tablename__ = 'audio'

    id = db.Column('AUDIO_ID', db.Integer, primary_key=True)
    user_id = db.Column('USER_ID', db.Integer, db.ForeignKey('usuario.ID'), nullable=False)
    audio_url = db.Column('AUDIO_URL', db.String(255))

    usuario = db.relationship('Usuario', backref=db.backref('audios', lazy=True))
    
    def __init__(self, user_id, audio_url):
        self.user_id = user_id
        self.audio_url = audio_url
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Foto(db.Model):
    __tablename__ = 'foto'

    id = db.Column('FOTO_ID', db.Integer, primary_key=True)
    user_id = db.Column('USER_ID', db.Integer, db.ForeignKey('usuario.ID'), nullable=False)
    foto_url = db.Column('FOTO_URL', db.String(255))

    usuario = db.relationship('Usuario', backref=db.backref('fotos', lazy=True))
    
    def __init__(self, user_id, foto_url):
        self.user_id = user_id
        self.foto_url = foto_url
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Video(db.Model):
    __tablename__ = 'video'

    id = db.Column('VIDEO_ID', db.Integer, primary_key=True)
    user_id = db.Column('USER_ID', db.Integer, db.ForeignKey('usuario.ID'), nullable=False)
    video_url = db.Column('VIDEO_URL', db.String(255))

    usuario = db.relationship('Usuario', backref=db.backref('videos', lazy=True))
    
    def __init__(self, user_id, video_url):
        self.user_id = user_id
        self.video_url = video_url
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    
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
    busca_instrumento = db.Column(db.String(255), nullable=False)
    instrumentos = db.Column(db.String(255), nullable=True)

    def __init__(self, tipo, nombre, email, contraseña, direccion, genero_musical, busca_genero,
                 busca_instrumento):
        super().__init__(tipo, nombre, email, contraseña, direccion, genero_musical, busca_genero)
        self.busca_instrumento = busca_instrumento
        self.instrumentos = None

# Clase Match
class Match(db.Model):
    __tablename__ = 'match_table'

    match_id = db.Column(db.Integer, primary_key=True)
    musico_id = db.Column(db.Integer, db.ForeignKey('musico.id'), nullable=False)
    grupo_id = db.Column(db.Integer, db.ForeignKey('grupo.id'), nullable=False)
    
    def save(self):
        db.session.add(self)
        db.session.commit()

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

    emisor = db.relationship('Usuario', foreign_keys=[emisor_id])
    receptor = db.relationship('Usuario', foreign_keys=[receptor_id])
    
    def save(self):
        db.session.add(self)
        db.session.commit()

class Dislike(db.Model):
    __tablename__ = 'dislike_table'

    dislike_id = db.Column(db.Integer, primary_key=True)
    emisor_id = db.Column(db.Integer, db.ForeignKey('usuario.ID'), nullable=False)
    receptor_id = db.Column(db.Integer, db.ForeignKey('usuario.ID'), nullable=False)
    
    emisor = db.relationship('Usuario', foreign_keys=[emisor_id])
    receptor = db.relationship('Usuario', foreign_keys=[receptor_id])
    
    def save(self):
        db.session.add(self)
        db.session.commit()

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
        if response['status'] == 'OK' and 'results' in response: 
            location = response['results'][0]['geometry']['location']
            return location
        return None
    
    def buscar_ciudad(self,direccion):
        #llamada a la API de Google Maps
        API_KEY='AIzaSyAO-2U9g7LQ0fHvkI4IfDBL_adMQflkcV4'
        params = {
        'key': API_KEY,
        'address': direccion}
        url = 'https://maps.googleapis.com/maps/api/geocode/json?'
        response = requests.get(url, params=params).json()
        response.keys()
        if response['status'] == 'OK' and 'results' in response: 
            ciudad = response['results'][0]['address_components'][2]['long_name']
            return ciudad
        return None