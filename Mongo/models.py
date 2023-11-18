from mongoengine import Document, StringField, ReferenceField, ListField, CASCADE
# from db_mongo import URI
# from mongoengine import connect
#
# connect(host=URI)


class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=150)
    description = StringField()
    meta = {"collection": "authors"}


class Quote(Document):
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=500))
    quote = StringField()
    meta = {"collection": "quotes"}
