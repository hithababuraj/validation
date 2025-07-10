from mongoengine import Document,StringField,IntField,EmailField,DateTimeField
from datetime import datetime

class Organisation(Document):
    org_name=StringField(required=True)
    org_description=StringField(required=True)
    org_code=IntField()
    created_date = DateTimeField(default=datetime.utcnow)
    update_date = DateTimeField(default=datetime.utcnow)
