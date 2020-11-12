import factory

from spaceone.core import utils
from spaceone.config.model.domain_config_model import DomainConfig


class DomainConfigFactory(factory.mongoengine.MongoEngineFactory):

    class Meta:
        model = DomainConfig

    name = factory.LazyAttribute(lambda o: utils.random_string())
    data = {
        'key': 'value',
        'key2': {
            'key3': 'value3'
        }
    }
    schema = factory.LazyAttribute(lambda o: utils.random_string())
    tags = {
        'key': 'value'
    }
    domain_id = utils.generate_id('domain')
    created_at = factory.Faker('date_time')
