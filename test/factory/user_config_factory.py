import factory

from spaceone.core import utils
from spaceone.config.model.user_config_model import UserConfig


class UserConfigFactory(factory.mongoengine.MongoEngineFactory):

    class Meta:
        model = UserConfig

    name = factory.LazyAttribute(lambda o: utils.random_string())
    data = {
        'key': 'value',
        'key2': {
            'key3': 'value3'
        }
    }
    tags = [
        {
            'key': 'tag_key',
            'value': 'tag_value'
        }
    ]
    domain_id = utils.generate_id('domain')
    user_id = utils.generate_id('user')
    updated_at = factory.Faker('date_time')
    created_at = factory.Faker('date_time')
