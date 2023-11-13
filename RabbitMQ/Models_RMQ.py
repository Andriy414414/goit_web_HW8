from mongoengine import Document, StringField, BooleanField


class Contact(Document):
    fullname = StringField(required=True, unique=True)
    email = StringField(max_length=100)
    send_status = BooleanField(default=False)
    meta = {"collection": "contacts"}