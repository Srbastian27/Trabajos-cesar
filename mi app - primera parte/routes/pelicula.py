from flask import request
from models.pelicula import Pelicula
from app import app, db
from models.genero import Genero
from bson.objectid import ObjectId 
from flask import render_template, request, jsonify 

@app.route("/pelicula/", methods=['POST'])
def addPelicula():
    try:
        mensaje=None
        estado=False
        if request.method== 'POST':
            datos = request.get_json(force=True)
            genero = Genero.objects(id=ObjectId(datos['genero'])).first()
            print(genero)
            if genero is not None:
                
                pelicula= Pelicula(**datos)
                pelicula.save()
                estado=True
                mensaje="Pelicula Agregada Correctamente"
        else:
            mensaje="No permitido"
        
    except Exception as error:
        mensaje=str(error)
        if "duplicate key" in mensaje:
            mensaje="No se puede agregar, el codigo de la pelicula ya existe"
            
    return {"estado": estado, "mensaje": mensaje}

@app.route("/pelicula/", methods=['GET'])
def listPeliculas():
    try:
        mensaje=None
        peliculas=Pelicula.objects()
        
    except Exception as error:
        mensaje=str(error)
        
    return {"mensaje": mensaje, "peliculas": peliculas}

@app.route("/pelicula/", method=['PUT'])
def updatePelicula():
    try:
        mensaje=None
        estado= False
        if request.method=='PUT':
            datos= request.get_json(force=True)
            pelicula = Pelicula.objects(id=ObjectId(datos['id'])).first()   
            if(pelicula is not None):
                pelicula.codigo=datos['codigo']
                pelicula.titulo=datos['titulo']
                pelicula.protagonista=datos['protagonista']
                pelicula.duracion=datos['duracion']
                pelicula.foto=datos['foto']
                pelicula.genero=datos['genero']
                pelicula.genero=ObjectId(datos['genero'])
                pelicula.save()
                estado=True 
                mensaje="Pelicula Actualizada...."
            else:
                mensaje="No existe pelicula para el id "    
    except Exception as error:
        mensaje=str(error) 
        
@app.route("/pelicula/", methods=['DELETE'])
def deletePeliculas():
    try:
        mensaje, estado = None,False
        if request.method=='GET':
            pelicula = Pelicula.objects(id=id).first()
            if(pelicula is not None):
                pelicula.delete()
                estado=True
            mensaje = "Pelicula Eliminada"
        else:
            mensaje = "No existe esta pelicula...."
            
    except Exception as error:
        mensaje=str(error) 
        
    return {"estado": estado, "mensaje": mensaje}
        
@app.route("/pelicula/", methods=['GET'])
def vistaAgregarPelicula():
    generos = Genero.objects()
    return render_template("frmAgregarPelicula.html", generos=generos)

        
    