from mongoengine import *

from spaceone.core.model.mongo_model import MongoModel


class PublicConfig(MongoModel):
    name = StringField(max_length=255, unique_with=["domain_id", "workspace_id", "project_id"])
    data = DictField()
    tags = DictField()
    resource_group = StringField(max_length=40, choices=("DOMAIN", "WORKSPACE", "PROJECT"))
    project_id = StringField(max_length=40)
    workspace_id = StringField(max_length=40)
    domain_id = StringField(max_length=40)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    meta = {
        "updatable_fields": ["name", "data", "tags", "updated_at"],
        "minimal_fields": ["name", "resource_group"],
        "change_query_keys": {"user_projects": "project_id"},
        "ordering": ["name"],
        "indexes": [
            "name",
            "domain_id",
            "workspace_id",
        ],
    }
