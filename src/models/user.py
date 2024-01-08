import mongoengine

from src.models.expense import Expense


class User(mongoengine.Document):
    username = mongoengine.StringField(required=True, min_length=1, unique=True)
    password = mongoengine.StringField(required=True)

    expenses = mongoengine.EmbeddedDocumentListField(Expense)

    meta = {
        "db_alias": "core",
        "collection": "users"
    }
