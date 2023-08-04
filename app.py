from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy


# Crear una instancia de la aplicación Flask
app = Flask(__name__)

""" # Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymsql://root:psswrd@localhost/bandmate'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
# Inicializar la base de datos
db = SQLAlchemy(app)
 """
# Rutas de la aplicación
@app.route('/')
def portada():
    return render_template('portada.html')

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)