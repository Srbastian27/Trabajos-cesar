from flask import Flask, render_template 
from flask_mongoengine import MongoEngine
from dotenv import load_dotenv
import os


from routes.genero import genero_bp
from routes.pelicula import pelicula_bp

load_dotenv()

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = './static/image'

app.config['MONGODB_SETTINGS'] = [
    {
        "db": "GestionPeliculas",
        "host": os.environ.get("URI"),
        "port": 27017
    }
]

db = MongoEngine(app)


app.register_blueprint(genero_bp)
app.register_blueprint(pelicula_bp)


@app.route("/")
def inicio():
    return render_template("contenido.html")

if __name__ == '__main__':
    app.run(port=5400, host='0.0.0.0', debug=True)