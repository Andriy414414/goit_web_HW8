from mongoengine import connect, Document, StringField, ReferenceField, ListField, CASCADE
from db import connect


class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=150)
    description = StringField()
    meta = {"collection": "author"}
