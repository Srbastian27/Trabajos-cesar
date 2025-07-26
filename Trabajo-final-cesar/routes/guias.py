from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models.guia import Guia

guias_bp = Blueprint('guias', __name__, url_prefix='/guias')

@guias_bp.route('/subir', methods=['GET', 'POST'])
@login_required
def subir():
    if request.method == 'POST':
        archivo = request.files['archivo']
        if archivo and archivo.filename.endswith('.pdf'):
            guia = Guia(
                nombre=request.form['nombre'],
                descripcion=request.form['descripcion'],
                programa=request.form['programa'],
                archivo=archivo.read(),
                instructor=current_user,
                regional=current_user.regional
            ).save()
            flash('Guía subida exitosamente', 'success')
            return redirect(url_for('guias.listar'))
    return render_template('guias/subir.html')
