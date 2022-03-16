import unittest
import copy
from unittest.mock import patch
from mongoengine import connect, disconnect
from google.protobuf.json_format import MessageToDict
from google.protobuf.empty_pb2 import Empty

from spaceone.core.unittest.result import print_message
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core import config
from spaceone.core import utils
from spaceone.core.service import BaseService
from spaceone.core.locator import Locator
from spaceone.core.pygrpc import BaseAPI
from spaceone.api.config.v1 import user_config_pb2
from spaceone.config.api.v1.user_config import UserConfig
from test.factory.user_config_factory import UserConfigFactory


class _MockUserConfigService(BaseService):

    def create(self, params):
        params = copy.deepcopy(params)
        if 'tags' in params:
            params['tags'] = utils.dict_to_tags(params['tags'])

        return UserConfigFactory(**params)

    def update(self, params):

        params = copy.deepcopy(params)
        if 'tags' in params:
            params['tags'] = utils.dict_to_tags(params['tags'])

        return UserConfigFactory(**params)

    def set(self, params):
        params = copy.deepcopy(params)
        if 'tags' in params:
            params['tags'] = utils.dict_to_tags(params['tags'])

        return UserConfigFactory(**params)

    def delete(self, params):
        pass

    def get(self, params):
        return UserConfigFactory(**params)

    def list(self, params):
        return UserConfigFactory.build_batch(10, **params), 10

    def stat(self, params):
        return {
            'result': [{'name': utils.random_string(), 'config_count': 100}]
        }


class TestUserConfigAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config.init_conf(package='spaceone.config')
        connect('test', host='mongomock://localhost')
        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        disconnect()

    @patch.object(BaseAPI, '__init__', return_value=None)
    @patch.object(Locator, 'get_service', return_value=_MockUserConfigService())
    @patch.object(BaseAPI, 'parse_request')
    def test_create_user_config(self, mock_parse_request, *args):
        params = {
            'name': utils.random_string(),
            'data': {
                'config_key': 'config_value'
            },
            'tags': {
                utils.random_string(): utils.random_string()
            },
            'domain_id': utils.generate_id('domain')
        }
        mock_parse_request.return_value = (params, {})

        user_config_servicer = UserConfig()
        user_config_info = user_config_servicer.create({}, {})

        print_message(user_config_info, 'test_create_user_config')
        user_config_data = MessageToDict(user_config_info, preserving_proto_field_name=True)

        self.assertIsInstance(user_config_info, user_config_pb2.UserConfigInfo)
        self.assertEqual(user_config_info.name, params['name'])
        self.assertDictEqual(MessageToDict(user_config_info.data), params['data'])
        self.assertDictEqual(user_config_data['tags'], params['tags'])
        self.assertEqual(user_config_info.domain_id, params['domain_id'])
        self.assertIsNotNone(getattr(user_config_info, 'created_at', None))
        self.assertIsNotNone(getattr(user_config_info, 'updated_at', None))

    @patch.object(BaseAPI, '__init__', return_value=None)
    @patch.object(Locator, 'get_service', return_value=_MockUserConfigService())
    @patch.object(BaseAPI, 'parse_request')
    def test_update_user_config(self, mock_parse_request, *args):
        params = {
            'name': utils.random_string(),
            'data': {
                'update_config_key': 'update_config_value'
            },
            'tags': {
                'update_key': 'update_value'
            },
            'domain_id': utils.generate_id('domain')
        }
        mock_parse_request.return_value = (params, {})

        user_config_servicer = UserConfig()
        user_config_info = user_config_servicer.update({}, {})

        print_message(user_config_info, 'test_update_user_config')
        user_config_data = MessageToDict(user_config_info, preserving_proto_field_name=True)

        self.assertIsInstance(user_config_info, user_config_pb2.UserConfigInfo)
        self.assertDictEqual(MessageToDict(user_config_info.data), params['data'])
        self.assertDictEqual(user_config_data['tags'], params['tags'])

    @patch.object(BaseAPI, '__init__', return_value=None)
    @patch.object(Locator, 'get_service', return_value=_MockUserConfigService())
    @patch.object(BaseAPI, 'parse_request')
    def test_set_user_config(self, mock_parse_request, *args):
        params = {
            'name': utils.random_string(),
            'data': {
                'config_key': 'config_value'
            },
            'tags': {
                utils.random_string(): utils.random_string()
            },
            'domain_id': utils.generate_id('domain')
        }
        mock_parse_request.return_value = (params, {})

        user_config_servicer = UserConfig()
        user_config_info = user_config_servicer.create({}, {})

        print_message(user_config_info, 'test_update_user_config')
        user_config_data = MessageToDict(user_config_info, preserving_proto_field_name=True)

        self.assertIsInstance(user_config_info, user_config_pb2.UserConfigInfo)
        self.assertEqual(user_config_info.name, params['name'])
        self.assertDictEqual(MessageToDict(user_config_info.data), params['data'])
        self.assertDictEqual(user_config_data['tags'], params['tags'])
        self.assertEqual(user_config_info.domain_id, params['domain_id'])
        self.assertIsNotNone(getattr(user_config_info, 'created_at', None))
        self.assertIsNotNone(getattr(user_config_info, 'updated_at', None))

    @patch.object(BaseAPI, '__init__', return_value=None)
    @patch.object(Locator, 'get_service', return_value=_MockUserConfigService())
    @patch.object(BaseAPI, 'parse_request')
    def test_delete_user_config(self, mock_parse_request, *args):
        mock_parse_request.return_value = ({}, {})

        user_config_servicer = UserConfig()
        result = user_config_servicer.delete({}, {})

        print_message(result, 'test_delete_user_config')

        self.assertIsInstance(result, Empty)

    @patch.object(BaseAPI, '__init__', return_value=None)
    @patch.object(Locator, 'get_service', return_value=_MockUserConfigService())
    @patch.object(BaseAPI, 'parse_request')
    def test_get_user_config(self, mock_parse_request, *args):
        mock_parse_request.return_value = ({}, {})

        user_config_servicer = UserConfig()
        user_config_info = user_config_servicer.get({}, {})

        print_message(user_config_info, 'test_get_user_config')

        self.assertIsInstance(user_config_info, user_config_pb2.UserConfigInfo)

    @patch.object(BaseAPI, '__init__', return_value=None)
    @patch.object(Locator, 'get_service', return_value=_MockUserConfigService())
    @patch.object(BaseAPI, 'parse_request')
    def test_list_user_configs(self, mock_parse_request, *args):
        mock_parse_request.return_value = ({}, {})

        user_config_servicer = UserConfig()
        user_configs_info = user_config_servicer.list({}, {})

        print_message(user_configs_info, 'test_list_user_configs')

        self.assertIsInstance(user_configs_info, user_config_pb2.UserConfigsInfo)
        self.assertIsInstance(user_configs_info.results[0], user_config_pb2.UserConfigInfo)
        self.assertEqual(user_configs_info.total_count, 10)

    @patch.object(BaseAPI, '__init__', return_value=None)
    @patch.object(Locator, 'get_service', return_value=_MockUserConfigService())
    @patch.object(BaseAPI, 'parse_request')
    def test_stat_user_configs(self, mock_parse_request, *args):
        mock_parse_request.return_value = ({}, {})

        user_config_servicer = UserConfig()
        stat_info = user_config_servicer.stat({}, {})
        print_message(stat_info, 'test_stat_user_configs')


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
