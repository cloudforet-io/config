from mongoengine import *

from spaceone.core.model.mongo_model import MongoModel


class DomainConfig(MongoModel):
    name = StringField(max_length=255, unique_with='domain_id')
    data = DictField()
    schema = StringField(max_length=64)
    tags = DictField()
    domain_id = StringField(max_length=255)
    created_at = DateTimeField(auto_now_add=True)

    meta = {
        'updatable_fields': [
            'name',
            'data',
            'schema',
            'tags'
        ],
        'exact_fields': [
            'domain_id'
        ],
        'minimal_fields': [
            'name'
        ],
        'ordering': [
            'name'
        ],
        'indexes': [
            'name',
            'domain_id'
        ]
    }
