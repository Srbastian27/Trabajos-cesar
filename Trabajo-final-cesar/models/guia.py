from mongoengine import Document, StringField, BinaryField, DateTimeField, ReferenceField
from datetime import datetime

class Guia(Document):
    nombre = StringField(required=True)
    descripcion = StringField(required=True)
    programa = StringField(required=True)
    archivo = BinaryField(required=True)
    instructor = ReferenceField('Instructor', reverse_delete_rule=2)  # Referencia al modelo Instructor
    regional = StringField(required=True)
    fecha = DateTimeField(default=datetime.utcnow)
