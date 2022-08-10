import unittest
from unittest.mock import patch
from mongoengine import connect, disconnect

from spaceone.core.unittest.result import print_data
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core import config
from spaceone.core import utils
from spaceone.core.model.mongo_model import MongoModel
from spaceone.core.transaction import Transaction
from spaceone.config.service.domain_config_service import DomainConfigService
from spaceone.config.model.domain_config_model import DomainConfig
from spaceone.config.info.domain_config_info import *
from spaceone.config.info.common_info import StatisticsInfo
from test.factory.domain_config_factory import DomainConfigFactory


class TestDomainConfigService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config.init_conf(package='spaceone.config')
        connect('test', host='mongomock://localhost')

        cls.domain_id = utils.generate_id('domain')
        cls.transaction = Transaction({
            'service': 'config',
            'api_class': 'DomainConfig'
        })
        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        disconnect()

    @patch.object(MongoModel, 'connect', return_value=None)
    def tearDown(self, *args) -> None:
        print()
        print('(tearDown) ==> Delete all config maps')
        domain_config_vos = DomainConfig.objects.filter()
        domain_config_vos.delete()

    @patch.object(MongoModel, 'connect', return_value=None)
    def test_create_domain_config(self, *args):
        params = {
            'name': 'inventory.server.metadata.view.table.layout',
            'data': {
                'key': 'value'
            },
            'tags': {
                utils.random_string(): utils.random_string()
            },
            'domain_id': utils.generate_id('domain')
        }

        self.transaction.method = 'create'
        domain_config_svc = DomainConfigService(transaction=self.transaction)
        domain_config_vo = domain_config_svc.create(params.copy())

        print_data(domain_config_vo.to_dict(), 'test_create_domain_config')
        DomainConfigInfo(domain_config_vo)

        self.assertIsInstance(domain_config_vo, DomainConfig)
        self.assertEqual(params['name'], domain_config_vo.name)
        self.assertEqual(params['data'], domain_config_vo.data)
        self.assertEqual(params['tags'], domain_config_vo.tags)
        self.assertEqual(params['domain_id'], domain_config_vo.domain_id)

    @patch.object(MongoModel, 'connect', return_value=None)
    def test_update_domain_config(self, *args):
        new_domain_config_vo = DomainConfigFactory(domain_id=self.domain_id)

        params = {
            'name': new_domain_config_vo.name,
            'data': {
                'update_data_key': 'update_data_value'
            },
            'tags': {
                'update_key': 'update_value'
            },
            'domain_id': self.domain_id
        }

        self.transaction.method = 'update'
        domain_config_svc = DomainConfigService(transaction=self.transaction)
        domain_config_vo = domain_config_svc.update(params.copy())

        print_data(domain_config_vo.to_dict(), 'test_update_domain_config')
        DomainConfigInfo(domain_config_vo)

        self.assertIsInstance(domain_config_vo, DomainConfig)
        self.assertEqual(params['data'], domain_config_vo.data)
        self.assertEqual(params['tags'], domain_config_vo.tags)
        self.assertEqual(params['domain_id'], domain_config_vo.domain_id)

    @patch.object(MongoModel, 'connect', return_value=None)
    def test_set_domain_config(self, *args):
        params = {
            'name': 'inventory.server.metadata.view.table.layout',
            'data': {
                'key': 'value'
            },
            'tags': {
                utils.random_string(): utils.random_string()
            },
            'domain_id': utils.generate_id('domain')
        }

        self.transaction.method = 'set'
        domain_config_svc = DomainConfigService(transaction=self.transaction)
        domain_config_vo = domain_config_svc.create(params.copy())

        print_data(domain_config_vo.to_dict(), 'test_set_domain_config')
        DomainConfigInfo(domain_config_vo)

        self.assertIsInstance(domain_config_vo, DomainConfig)
        self.assertEqual(params['name'], domain_config_vo.name)
        self.assertEqual(params['data'], domain_config_vo.data)
        self.assertEqual(params['tags'], domain_config_vo.tags)
        self.assertEqual(params['domain_id'], domain_config_vo.domain_id)

    @patch.object(MongoModel, 'connect', return_value=None)
    def test_delete_domain_config(self, *args):
        new_domain_config_vo = DomainConfigFactory(domain_id=self.domain_id)

        params = {
            'name': new_domain_config_vo.name,
            'domain_id': self.domain_id
        }

        self.transaction.method = 'delete'
        domain_config_svc = DomainConfigService(transaction=self.transaction)
        result = domain_config_svc.delete(params.copy())

        self.assertIsNone(result)

    @patch.object(MongoModel, 'connect', return_value=None)
    def test_get_domain_config(self, *args):
        new_domain_config_vo = DomainConfigFactory(domain_id=self.domain_id)

        params = {
            'name': new_domain_config_vo.name,
            'domain_id': self.domain_id
        }

        self.transaction.method = 'get'
        domain_config_svc = DomainConfigService(transaction=self.transaction)
        domain_config_vo = domain_config_svc.get(params.copy())

        print_data(domain_config_vo.to_dict(), 'test_get_domain_config')
        DomainConfigInfo(domain_config_vo)

        self.assertIsInstance(domain_config_vo, DomainConfig)

    @patch.object(MongoModel, 'connect', return_value=None)
    def test_list_domain_configs_by_name(self, *args):
        domain_config_vos = DomainConfigFactory.build_batch(10, domain_id=self.domain_id)
        list(map(lambda vo: vo.save(), domain_config_vos))

        params = {
            'name': domain_config_vos[0].name,
            'domain_id': self.domain_id
        }

        self.transaction.method = 'list'
        domain_config_svc = DomainConfigService(transaction=self.transaction)
        domain_config_vos, total_count = domain_config_svc.list(params.copy())
        DomainConfigsInfo(domain_config_vos, total_count)

        self.assertEqual(len(domain_config_vos), 1)
        self.assertIsInstance(domain_config_vos[0], DomainConfig)
        self.assertEqual(total_count, 1)

    @patch.object(MongoModel, 'connect', return_value=None)
    def test_list_domain_configs_by_tag(self, *args):
        DomainConfigFactory(tags={'tag_key_1': 'tag_value_1'}, domain_id=self.domain_id)
        domain_config_vos = DomainConfigFactory.build_batch(9, domain_id=self.domain_id)
        list(map(lambda vo: vo.save(), domain_config_vos))

        params = {
            'query': {
                'filter': [{
                    'k': 'tags.tag_key_1',
                    'v': 'tag_value_1',
                    'o': 'eq'
                }]
            },
            'domain_id': self.domain_id
        }

        self.transaction.method = 'list'
        domain_config_svc = DomainConfigService(transaction=self.transaction)
        domain_config_vos, total_count = domain_config_svc.list(params.copy())
        DomainConfigsInfo(domain_config_vos, total_count)

        self.assertEqual(len(domain_config_vos), 1)
        self.assertIsInstance(domain_config_vos[0], DomainConfig)
        self.assertEqual(total_count, 1)

    @patch.object(MongoModel, 'connect', return_value=None)
    def test_stat_domain_configs(self, *args):
        domain_config_vos = DomainConfigFactory.build_batch(10, domain_id=self.domain_id)
        list(map(lambda vo: vo.save(), domain_config_vos))

        params = {
            'domain_id': self.domain_id,
            'query': {
                'aggregate': [{
                    'group': {
                        'keys': [{
                            'key': 'name',
                            'name': 'Name'
                        }],
                        'fields': [{
                            'operator': 'count',
                            'name': 'Count'
                        }]
                    }
                }, {
                    'sort': {
                        'key': 'Count',
                        'desc': True
                    }
                }]
            }
        }

        self.transaction.method = 'stat'
        domain_config_svc = DomainConfigService(transaction=self.transaction)
        values = domain_config_svc.stat(params)
        StatisticsInfo(values)

        print_data(values, 'test_stat_domain_configs')

    @patch.object(MongoModel, 'connect', return_value=None)
    def test_stat_domain_configs_distinct(self, *args):
        domain_config_vos = DomainConfigFactory.build_batch(10, domain_id=self.domain_id)
        list(map(lambda vo: vo.save(), domain_config_vos))

        params = {
            'domain_id': self.domain_id,
            'query': {
                'distinct': 'name',
                'page': {
                    'start': 2,
                    'limit': 3
                }
            }
        }

        self.transaction.method = 'stat'
        domain_config_svc = DomainConfigService(transaction=self.transaction)
        values = domain_config_svc.stat(params)
        StatisticsInfo(values)

        print_data(values, 'test_stat_domain_configs_distinct')


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
