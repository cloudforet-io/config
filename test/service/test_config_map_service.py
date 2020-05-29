import unittest
from unittest.mock import patch
from mongoengine import connect, disconnect

from spaceone.core.unittest.result import print_data
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core import config
from spaceone.core import utils
from spaceone.core.model.mongo_model import MongoModel
from spaceone.core.transaction import Transaction
from spaceone.config.service.config_map_service import ConfigMapService
from spaceone.config.model.config_map_model import ConfigMap
from spaceone.config.info.config_map_info import *
from spaceone.config.info.common_info import StatisticsInfo
from test.factory.config_map_factory import ConfigMapFactory


class TestConfigMapService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config.init_conf(service='config')
        connect('test', host='mongomock://localhost')

        cls.domain_id = utils.generate_id('domain')
        cls.transaction = Transaction({
            'service': 'config',
            'api_class': 'ConfigMap'
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
        config_map_vos = ConfigMap.objects.filter()
        config_map_vos.delete()

    @patch.object(MongoModel, 'connect', return_value=None)
    def test_create_config_map(self, *args):
        params = {
            'name': 'inventory.server.metadata.view.table.layout',
            'data': {
                'key': 'value'
            },
            'tags': {
                'key': 'value'
            },
            'domain_id': utils.generate_id('domain')
        }

        self.transaction.method = 'create'
        config_map_svc = ConfigMapService(transaction=self.transaction)
        config_map_vo = config_map_svc.create(params.copy())

        print_data(config_map_vo.to_dict(), 'test_create_config_map')
        ConfigMapInfo(config_map_vo)

        self.assertIsInstance(config_map_vo, ConfigMap)
        self.assertEqual(params['name'], config_map_vo.name)
        self.assertEqual(params['data'], config_map_vo.data)
        self.assertEqual(params.get('tags', {}), config_map_vo.tags)
        self.assertEqual(params['domain_id'], config_map_vo.domain_id)

    @patch.object(MongoModel, 'connect', return_value=None)
    def test_update_config_map(self, *args):
        new_config_map_vo = ConfigMapFactory(domain_id=self.domain_id)

        params = {
            'name': new_config_map_vo.name,
            'data': {
                'update_data_key': 'update_data_value'
            },
            'tags': {
                'update_key': 'update_value'
            },
            'domain_id': self.domain_id
        }

        self.transaction.method = 'update'
        config_map_svc = ConfigMapService(transaction=self.transaction)
        config_map_vo = config_map_svc.update(params.copy())

        print_data(config_map_vo.to_dict(), 'test_update_config_map')
        ConfigMapInfo(config_map_vo)

        self.assertIsInstance(config_map_vo, ConfigMap)
        self.assertEqual(params['data'], config_map_vo.data)
        self.assertEqual(params.get('tags', {}), config_map_vo.tags)
        self.assertEqual(params['domain_id'], config_map_vo.domain_id)

    @patch.object(MongoModel, 'connect', return_value=None)
    def test_delete_config_map(self, *args):
        new_config_map_vo = ConfigMapFactory(domain_id=self.domain_id)

        params = {
            'name': new_config_map_vo.name,
            'domain_id': self.domain_id
        }

        self.transaction.method = 'delete'
        config_map_svc = ConfigMapService(transaction=self.transaction)
        result = config_map_svc.delete(params.copy())

        self.assertIsNone(result)

    @patch.object(MongoModel, 'connect', return_value=None)
    def test_get_config_map(self, *args):
        new_config_map_vo = ConfigMapFactory(domain_id=self.domain_id)

        params = {
            'name': new_config_map_vo.name,
            'domain_id': self.domain_id
        }

        self.transaction.method = 'get'
        config_map_svc = ConfigMapService(transaction=self.transaction)
        config_map_vo = config_map_svc.get(params.copy())

        print_data(config_map_vo.to_dict(), 'test_get_config_map')
        ConfigMapInfo(config_map_vo)

        self.assertIsInstance(config_map_vo, ConfigMap)

    @patch.object(MongoModel, 'connect', return_value=None)
    def test_list_config_maps_by_name(self, *args):
        config_map_vos = ConfigMapFactory.build_batch(10, domain_id=self.domain_id)
        list(map(lambda vo: vo.save(), config_map_vos))

        params = {
            'name': config_map_vos[0].name,
            'domain_id': self.domain_id
        }

        self.transaction.method = 'list'
        config_map_svc = ConfigMapService(transaction=self.transaction)
        config_map_vos, total_count = config_map_svc.list(params.copy())
        ConfigMapsInfo(config_map_vos, total_count)

        self.assertEqual(len(config_map_vos), 1)
        self.assertIsInstance(config_map_vos[0], ConfigMap)
        self.assertEqual(total_count, 1)

    @patch.object(MongoModel, 'connect', return_value=None)
    def test_list_config_maps_by_tag(self, *args):
        ConfigMapFactory(tags={'tag_key': 'tag_value'}, domain_id=self.domain_id)
        config_map_vos = ConfigMapFactory.build_batch(9, domain_id=self.domain_id)
        list(map(lambda vo: vo.save(), config_map_vos))

        params = {
            'query': {
                'filter': [{
                    'k': 'tags.tag_key',
                    'v': 'tag_value',
                    'o': 'eq'
                }]
            },
            'domain_id': self.domain_id
        }

        self.transaction.method = 'list'
        config_map_svc = ConfigMapService(transaction=self.transaction)
        config_map_vos, total_count = config_map_svc.list(params.copy())
        ConfigMapsInfo(config_map_vos, total_count)

        self.assertEqual(len(config_map_vos), 1)
        self.assertIsInstance(config_map_vos[0], ConfigMap)
        self.assertEqual(total_count, 1)

    @patch.object(MongoModel, 'connect', return_value=None)
    def test_stat_config_maps(self, *args):
        config_map_vos = ConfigMapFactory.build_batch(10, domain_id=self.domain_id)
        list(map(lambda vo: vo.save(), config_map_vos))

        params = {
            'domain_id': self.domain_id,
            'query': {
                'aggregate': {
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
                },
                'sort': {
                    'name': 'Count',
                    'desc': True
                }
            }
        }

        self.transaction.method = 'stat'
        config_map_svc = ConfigMapService(transaction=self.transaction)
        values = config_map_svc.stat(params)
        StatisticsInfo(values)

        print_data(values, 'test_stat_config_maps')


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
