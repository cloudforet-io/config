import factory

from spaceone.core import utils
from spaceone.config.model.config_map_model import ConfigMap


class ConfigMapFactory(factory.mongoengine.MongoEngineFactory):

    class Meta:
        model = ConfigMap

    name = factory.LazyAttribute(lambda o: utils.random_string())
    data = {
        'key': 'value',
        'key2': {
            'key3': 'value3'
        }
    }
    tags = {
        'key': 'value'
    }
    domain_id = utils.generate_id('domain')
    created_at = factory.Faker('date_time')
