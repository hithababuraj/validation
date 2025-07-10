from mongoengine import StringField,EmailField,IntField,DateTimeField,Document
from datetime import datetime

class User(Document):
    name = StringField(required=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    age = IntField()
    created_at = DateTimeField(default=datetime.utcnow)




    