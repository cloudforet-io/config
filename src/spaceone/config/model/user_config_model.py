from mongoengine import *

from spaceone.core.model.mongo_model import MongoModel


class UserConfigTag(EmbeddedDocument):
    key = StringField(max_length=255)
    value = StringField(max_length=255)


class UserConfig(MongoModel):
    name = StringField(max_length=255, unique_with=['user_id', 'domain_id'])
    data = DictField()
    tags = ListField(EmbeddedDocumentField(UserConfigTag))
    user_id = StringField(max_length=40)
    domain_id = StringField(max_length=40)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    meta = {
        'updatable_fields': [
            'name',
            'data',
            'tags',
            'updated_at'
        ],
        'minimal_fields': [
            'name'
        ],
        'change_query_keys': {
            'user_self': 'user_id'
        },
        'ordering': [
            'name'
        ],
        'indexes': [
            'name',
            'user_id',
            'domain_id',
            ('tags.key', 'tags.value')
        ]
    }
