from mongoengine import Document, StringField, EmailField, DateTimeField
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class Instructor(Document):
    nombre = StringField(required=True)
    email = EmailField(required=True, unique=True)
    regional = StringField(required=True)
    password = StringField(required=True)
    fecha_registro = DateTimeField(default=datetime.utcnow)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
