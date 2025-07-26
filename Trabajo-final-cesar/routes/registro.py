from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.instructor import Instructor
from werkzeug.security import generate_password_hash
import secrets

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        try:
            password = secrets.token_urlsafe(8)
            instructor = Instructor(
                nombre=request.form['nombre'],
                email=request.form['email'],
                regional=request.form['regional']
            )
            instructor.set_password(password)
            instructor.save()
            # enviar_correo(instructor.email, password)
            flash('Registro exitoso. Revisa tu correo para las credenciales', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash(f'Error en el registro: {str(e)}', 'danger')
    return render_template('auth/registro.html')
