from app import db
from datetime import datetime

class Usuario(db.Model):
    __tablename__ = 'usuario'

    id = db.Column('ID', db.Integer, primary_key=True)
    tipo = db.Column('TIPO', db.String(6), nullable=False)
    nombre = db.Column('NOMBRE', db.String(255), nullable=False)
    email = db.Column('EMAIL', db.String(255), nullable=False)
    contraseña = db.Column('CONTRASEÑA', db.String(255), nullable=False)
    direccion = db.Column('DIRECCION', db.String(255), nullable=False)
    cancion_fav = db.Column('CANCION_FAV', db.String(255))
    genero_musical = db.Column('GENERO_MUSICAL', db.String(255))
    descripcion = db.Column('DESCRIPCION', db.String(255))
    busca_genero = db.Column('BUSCA_GENERO', db.String(255))
    busca_distancia = db.Column('BUSCA_DISTANCIA', db.Integer)
    longitud = db.Column('LONGITUD', db.Float)
    latitud = db.Column('LATITUD', db.Float)
    
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

    id = db.Column(db.Integer, db.ForeignKey('usuario.id'), primary_key=True)
    instrumento_principal = db.Column(db.String(255), nullable=False)
    sexo = db.Column(db.String(255), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    musico_id = db.Column(db.Integer, primary_key=True) 

class Grupo(Usuario):
    __tablename__ = 'grupo'

    id = db.Column(db.Integer, db.ForeignKey('usuario.id'), primary_key=True)
    busca_instrumento = db.Column(db.String(255), nullable=True)
    instrumentos = db.Column(db.String(255), nullable=True)
    grupo_id = db.Column(db.Integer, primary_key=True)  


# Clase Match
class Match(db.Model):
    __tablename__ = 'match_table'

    match_id = db.Column(db.Integer, primary_key=True)
    musico_id = db.Column(db.Integer, db.ForeignKey('musico.musico_id'), nullable=False)
    grupo_id = db.Column(db.Integer, db.ForeignKey('grupo.grupo_id'), nullable=False)



# Clase Mensaje
class Mensaje(db.Model):
    __tablename__ = 'mensaje'

    mensaje_id = db.Column(db.Integer, primary_key=True)
    emisor_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    receptor_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    texto = db.Column(db.String(255), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
class Like(db.Model):
    __tablename__ = 'like_table'

    like_id = db.Column(db.Integer, primary_key=True)
    emisor_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    receptor_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

class Dislike(db.Model):
    __tablename__ = 'dislike_table'

    dislike_id = db.Column(db.Integer, primary_key=True)
    emisor_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    receptor_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

