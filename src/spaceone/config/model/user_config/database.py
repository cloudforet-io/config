from mongoengine import *

from spaceone.core.model.mongo_model import MongoModel


class UserConfig(MongoModel):
    name = StringField(max_length=255, unique_with=["user_id", "domain_id"])
    data = DictField(default=None)
    tags = DictField(default=None)
    domain_id = StringField(max_length=40)
    user_id = StringField(max_length=40)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    meta = {
        "updatable_fields": ["name", "data", "tags", "updated_at"],
        "minimal_fields": ["name"],
        "ordering": ["name"],
        "indexes": [
            "name",
            "domain_id",
            "user_id",
        ],
    }
