from mongoengine import *

from spaceone.core.model.mongo_model import MongoModel


class SharedConfig(MongoModel):
    name = StringField(max_length=255, unique_with=["domain_id", "workspace_id", "project_id"])
    data = DictField(default=None)
    tags = DictField(default=None)
    resource_group = StringField(max_length=40, choices=("DOMAIN", "WORKSPACE", "PROJECT"))
    project_id = StringField(max_length=40)
    workspace_id = StringField(max_length=40)
    domain_id = StringField(max_length=40)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    meta = {
        "updatable_fields": ["name", "data", "tags"],
        "minimal_fields": ["name", "resource_group", "domain_id", "workspace_id", "project_id"],
        "change_query_keys": {"user_projects": "project_id"},
        "ordering": ["name"],
        "indexes": [
            "name",
            "domain_id",
            "workspace_id",
            "project_id"
        ],
    }
