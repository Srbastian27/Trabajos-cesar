from flask import Blueprint, render_template, request, jsonify
from models.genero import Genero # Esto sí lo necesitas para interactuar con el modelo
from bson.objectid import ObjectId

genero_bp = Blueprint('genero_bp', __name__)

@genero_bp.route("/generos/", methods=['GET'])
def listarGeneros():
    try:
        mensaje = ""
        generos = Genero.objects() # Esto ya funciona porque MongoEngine está inicializado
        return render_template("listarGeneros.html", generos=generos, mensaje=mensaje)
    except Exception as error:
        mensaje = str(error)
        return render_template("listarGeneros.html", generos=[], mensaje=mensaje)

@genero_bp.route("/genero/", methods=['POST'])
def addGenero():
    try:
        mensaje = None
        estado = False
        if request.method == 'POST':
            datos = request.get_json(force=True)
            genero = Genero(**datos)
            genero.save()
            estado = True
            mensaje = "Género agregado correctamente"
        else:
            mensaje = "Método no permitido"
        return jsonify({"estado": estado, "mensaje": mensaje})
    except Exception as error:
        mensaje = str(error)
        return jsonify({"estado": False, "mensaje": mensaje})

@genero_bp.route("/genero/<string:genero_id>", methods=['PUT'])
def editGenero(genero_id):
    try:
        mensaje = None
        estado = False
        if request.method == 'PUT':
            datos = request.get_json(force=True)
            genero_a_editar = Genero.objects(id=ObjectId(genero_id)).first()
            if genero_a_editar:
                if 'nombre' in datos:
                    genero_a_editar.nombre = datos['nombre']
                genero_a_editar.save()
                estado = True
                mensaje = "Género editado correctamente"
            else:
                mensaje = "Género no encontrado"
        else:
            mensaje = "Método no permitido"
        return jsonify({"estado": estado, "mensaje": mensaje})
    except Exception as error:
        mensaje = str(error)
        return jsonify({"estado": False, "mensaje": mensaje})

@genero_bp.route("/genero/<string:genero_id>", methods=['DELETE'])
def deleteGenero(genero_id):
    try:
        mensaje = None
        estado = False
        genero_a_eliminar = Genero.objects(id=ObjectId(genero_id)).first()
        if genero_a_eliminar:
            genero_a_eliminar.delete()
            estado = True
            mensaje = "Género eliminado correctamente"
        else:
            mensaje = "Género no encontrado"
        return jsonify({"estado": estado, "mensaje": mensaje})
    except Exception as error:
        mensaje = str(error)
        return jsonify({"estado": False, "mensaje": mensaje})