import os
import secrets
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Configuración MongoDB (tu código original)
MONGO_URI = os.getenv('MONGO_URI')
if not MONGO_URI:
    raise ValueError("La variable de entorno MONGO_URI no está configurada")

try:
    client = MongoClient(MONGO_URI)
    db = client.get_default_database()
    print("✅ Conexión exitosa a MongoDB Atlas")
    
    # Crear colecciones si no existen
    if 'instructores' not in db.list_collection_names():
        db.create_collection('instructores')
    if 'guias' not in db.list_collection_names():
        db.create_collection('guias')

except Exception as e:
    print(f"❌ Error de conexión: {e}")
    exit()

# Configuración Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, user_data):
        self.user_data = user_data
    
    def get_id(self):
        return str(self.user_data['_id'])

@login_manager.user_loader
def load_user(user_id):
    user = db.instructores.find_one({'_id': user_id})
    return User(user) if user else None

# Rutas principales
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        try:
            password = secrets.token_urlsafe(8)
            instructor = {
                "nombre": request.form['nombre'],
                "email": request.form['email'],
                "regional": request.form['regional'],
                "password": generate_password_hash(password),
                "fecha_registro": datetime.utcnow()
            }
            
            result = db.instructores.insert_one(instructor)
            print(f"📝 Instructor registrado ID: {result.inserted_id}")
            flash('Registro exitoso. Revisa tu correo para las credenciales', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            flash(f'Error en registro: {str(e)}', 'danger')
    
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = db.instructores.find_one({'email': email})
        
        if user and check_password_hash(user['password'], password):
            login_user(User(user))
            return redirect(url_for('subir_guia'))
        flash('Credenciales inválidas', 'danger')
    
    return render_template('login.html')

@app.route('/subir-guia', methods=['GET', 'POST'])
@login_required
def subir_guia():
    if request.method == 'POST':
        try:
            archivo = request.files['archivo']
            if archivo and archivo.filename.endswith('.pdf'):
                guia = {
                    "nombre": request.form['nombre'],
                    "descripcion": request.form['descripcion'],
                    "programa": request.form['programa'],
                    "archivo": archivo.read(),
                    "instructor_id": current_user.get_id(),
                    "fecha": datetime.utcnow(),
                    "regional": current_user.user_data['regional']
                }
                
                db.guias.insert_one(guia)
                flash('Guía subida exitosamente', 'success')
                return redirect(url_for('listar_guias'))
            
            flash('Solo se permiten archivos PDF', 'danger')
        except Exception as e:
            flash(f'Error al subir guía: {str(e)}', 'danger')
    
    return render_template('subir_guia.html')

@app.route('/guias')
@login_required
def listar_guias():
    guias = list(db.guias.find({'instructor_id': current_user.get_id()}))
    return render_template('listar_guias.html', guias=guias)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)


