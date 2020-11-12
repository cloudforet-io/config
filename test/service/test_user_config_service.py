import unittest
from unittest.mock import patch
from mongoengine import connect, disconnect

from spaceone.core.unittest.result import print_data
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core import config
from spaceone.core import utils
from spaceone.core.model.mongo_model import MongoModel
from spaceone.core.transaction import Transaction
from spaceone.config.service.user_config_service import UserConfigService
from spaceone.config.model.user_config_model import UserConfig
from spaceone.config.info.user_config_info import *
from spaceone.config.info.common_info import StatisticsInfo
from test.factory.user_config_factory import UserConfigFactory


class TestUserConfigService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config.init_conf(package='spaceone.config')
        connect('test', host='mongomock://localhost')

        cls.domain_id = utils.generate_id('domain')
        cls.transaction = Transaction({
            'service': 'config',
            'api_class': 'UserConfig'
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
        user_config_vos = UserConfig.objects.filter()
        user_config_vos.delete()

    @patch.object(MongoModel, 'connect', return_value=None)
    def test_create_user_config(self, *args):
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
        user_config_svc = UserConfigService(transaction=self.transaction)
        user_config_vo = user_config_svc.create(params.copy())

        print_data(user_config_vo.to_dict(), 'test_create_user_config')
        UserConfigInfo(user_config_vo)

        self.assertIsInstance(user_config_vo, UserConfig)
        self.assertEqual(params['name'], user_config_vo.name)
        self.assertEqual(params['data'], user_config_vo.data)
        self.assertEqual(params.get('tags', {}), user_config_vo.tags)
        self.assertEqual(params['domain_id'], user_config_vo.domain_id)

    @patch.object(MongoModel, 'connect', return_value=None)
    def test_update_user_config(self, *args):
        new_user_config_vo = UserConfigFactory(domain_id=self.domain_id)

        params = {
            'name': new_user_config_vo.name,
            'data': {
                'update_data_key': 'update_data_value'
            },
            'tags': {
                'update_key': 'update_value'
            },
            'domain_id': self.domain_id
        }

        self.transaction.method = 'update'
        user_config_svc = UserConfigService(transaction=self.transaction)
        user_config_vo = user_config_svc.update(params.copy())

        print_data(user_config_vo.to_dict(), 'test_update_user_config')
        UserConfigInfo(user_config_vo)

        self.assertIsInstance(user_config_vo, UserConfig)
        self.assertEqual(params['data'], user_config_vo.data)
        self.assertEqual(params.get('tags', {}), user_config_vo.tags)
        self.assertEqual(params['domain_id'], user_config_vo.domain_id)

    @patch.object(MongoModel, 'connect', return_value=None)
    def test_delete_user_config(self, *args):
        new_user_config_vo = UserConfigFactory(domain_id=self.domain_id)

        params = {
            'name': new_user_config_vo.name,
            'domain_id': self.domain_id
        }

        self.transaction.method = 'delete'
        user_config_svc = UserConfigService(transaction=self.transaction)
        result = user_config_svc.delete(params.copy())

        self.assertIsNone(result)

    @patch.object(MongoModel, 'connect', return_value=None)
    def test_get_user_config(self, *args):
        new_user_config_vo = UserConfigFactory(domain_id=self.domain_id)

        params = {
            'name': new_user_config_vo.name,
            'domain_id': self.domain_id
        }

        self.transaction.method = 'get'
        user_config_svc = UserConfigService(transaction=self.transaction)
        user_config_vo = user_config_svc.get(params.copy())

        print_data(user_config_vo.to_dict(), 'test_get_user_config')
        UserConfigInfo(user_config_vo)

        self.assertIsInstance(user_config_vo, UserConfig)

    @patch.object(MongoModel, 'connect', return_value=None)
    def test_list_user_configs_by_name(self, *args):
        user_config_vos = UserConfigFactory.build_batch(10, domain_id=self.domain_id)
        list(map(lambda vo: vo.save(), user_config_vos))

        params = {
            'name': user_config_vos[0].name,
            'domain_id': self.domain_id
        }

        self.transaction.method = 'list'
        user_config_svc = UserConfigService(transaction=self.transaction)
        user_config_vos, total_count = user_config_svc.list(params.copy())
        UserConfigsInfo(user_config_vos, total_count)

        self.assertEqual(len(user_config_vos), 1)
        self.assertIsInstance(user_config_vos[0], UserConfig)
        self.assertEqual(total_count, 1)

    @patch.object(MongoModel, 'connect', return_value=None)
    def test_list_user_configs_by_tag(self, *args):
        UserConfigFactory(tags={'tag_key': 'tag_value'}, domain_id=self.domain_id)
        user_config_vos = UserConfigFactory.build_batch(9, domain_id=self.domain_id)
        list(map(lambda vo: vo.save(), user_config_vos))

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
        user_config_svc = UserConfigService(transaction=self.transaction)
        user_config_vos, total_count = user_config_svc.list(params.copy())
        UserConfigsInfo(user_config_vos, total_count)

        self.assertEqual(len(user_config_vos), 1)
        self.assertIsInstance(user_config_vos[0], UserConfig)
        self.assertEqual(total_count, 1)

    @patch.object(MongoModel, 'connect', return_value=None)
    def test_stat_user_configs(self, *args):
        user_config_vos = UserConfigFactory.build_batch(10, domain_id=self.domain_id)
        list(map(lambda vo: vo.save(), user_config_vos))

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
        user_config_svc = UserConfigService(transaction=self.transaction)
        values = user_config_svc.stat(params)
        StatisticsInfo(values)

        print_data(values, 'test_stat_user_configs')

    @patch.object(MongoModel, 'connect', return_value=None)
    def test_stat_user_configs_distinct(self, *args):
        user_config_vos = UserConfigFactory.build_batch(10, domain_id=self.domain_id)
        list(map(lambda vo: vo.save(), user_config_vos))

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
        user_config_svc = UserConfigService(transaction=self.transaction)
        values = user_config_svc.stat(params)
        StatisticsInfo(values)

        print_data(values, 'test_stat_user_configs_distinct')


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
