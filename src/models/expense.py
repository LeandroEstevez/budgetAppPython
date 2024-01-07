import mongoengine
from bson import ObjectId


class Expense(mongoengine.EmbeddedDocument):
    id = mongoengine.ObjectIdField(default=ObjectId, primary_key=True)
    name = mongoengine.StringField(required=True, min_length=1)
    amount = mongoengine.DecimalField(required=True, precision=2, min_value=0)
    due_date = mongoengine.DateField(required=True)

    meta = {
        "db_alias": "core",
        "collection": "expenses"
    }
