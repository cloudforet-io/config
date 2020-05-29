import unittest
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
from spaceone.api.config.v1 import config_map_pb2
from spaceone.config.api.v1.config_map import ConfigMap
from test.factory.config_map_factory import ConfigMapFactory


class _MockConfigMapService(BaseService):

    def create(self, params):
        return ConfigMapFactory(**params)

    def update(self, params):
        return ConfigMapFactory(**params)

    def delete(self, params):
        pass

    def get(self, params):
        return ConfigMapFactory(**params)

    def list(self, params):
        return ConfigMapFactory.build_batch(10, **params), 10

    def stat(self, params):
        return [{'name': utils.random_string(), 'config_count': 100}]


class TestConfigMapAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config.init_conf(service='config')
        connect('test', host='mongomock://localhost')
        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        disconnect()

    @patch.object(BaseAPI, '__init__', return_value=None)
    @patch.object(Locator, 'get_service', return_value=_MockConfigMapService())
    @patch.object(BaseAPI, 'parse_request')
    def test_create_config_map(self, mock_parse_request, *args):
        params = {
            'name': utils.random_string(),
            'data': {
                'config_key': 'config_value'
            },
            'tags': {
                'tag_key': 'tag_value'
            },
            'domain_id': utils.generate_id('domain')
        }
        mock_parse_request.return_value = (params, {})

        config_map_servicer = ConfigMap()
        config_map_info = config_map_servicer.create({}, {})

        print_message(config_map_info, 'test_create_config_map')

        self.assertIsInstance(config_map_info, config_map_pb2.ConfigMapInfo)
        self.assertEqual(config_map_info.name, params['name'])
        self.assertDictEqual(MessageToDict(config_map_info.data), params['data'])
        self.assertDictEqual(MessageToDict(config_map_info.tags), params['tags'])
        self.assertEqual(config_map_info.domain_id, params['domain_id'])
        self.assertIsNotNone(getattr(config_map_info, 'created_at', None))

    @patch.object(BaseAPI, '__init__', return_value=None)
    @patch.object(Locator, 'get_service', return_value=_MockConfigMapService())
    @patch.object(BaseAPI, 'parse_request')
    def test_update_config_map(self, mock_parse_request, *args):
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

        config_map_servicer = ConfigMap()
        config_map_info = config_map_servicer.update({}, {})

        print_message(config_map_info, 'test_update_config_map')

        self.assertIsInstance(config_map_info, config_map_pb2.ConfigMapInfo)
        self.assertDictEqual(MessageToDict(config_map_info.data), params['data'])
        self.assertDictEqual(MessageToDict(config_map_info.tags), params['tags'])

    @patch.object(BaseAPI, '__init__', return_value=None)
    @patch.object(Locator, 'get_service', return_value=_MockConfigMapService())
    @patch.object(BaseAPI, 'parse_request')
    def test_delete_config_map(self, mock_parse_request, *args):
        mock_parse_request.return_value = ({}, {})

        config_map_servicer = ConfigMap()
        result = config_map_servicer.delete({}, {})

        print_message(result, 'test_delete_config_map')

        self.assertIsInstance(result, Empty)

    @patch.object(BaseAPI, '__init__', return_value=None)
    @patch.object(Locator, 'get_service', return_value=_MockConfigMapService())
    @patch.object(BaseAPI, 'parse_request')
    def test_get_config_map(self, mock_parse_request, *args):
        mock_parse_request.return_value = ({}, {})

        config_map_servicer = ConfigMap()
        config_map_info = config_map_servicer.get({}, {})

        print_message(config_map_info, 'test_get_config_map')

        self.assertIsInstance(config_map_info, config_map_pb2.ConfigMapInfo)

    @patch.object(BaseAPI, '__init__', return_value=None)
    @patch.object(Locator, 'get_service', return_value=_MockConfigMapService())
    @patch.object(BaseAPI, 'parse_request')
    def test_list_config_maps(self, mock_parse_request, *args):
        mock_parse_request.return_value = ({}, {})

        config_map_servicer = ConfigMap()
        config_maps_info = config_map_servicer.list({}, {})

        print_message(config_maps_info, 'test_list_config_maps')

        self.assertIsInstance(config_maps_info, config_map_pb2.ConfigMapsInfo)
        self.assertIsInstance(config_maps_info.results[0], config_map_pb2.ConfigMapInfo)
        self.assertEqual(config_maps_info.total_count, 10)

    @patch.object(BaseAPI, '__init__', return_value=None)
    @patch.object(Locator, 'get_service', return_value=_MockConfigMapService())
    @patch.object(BaseAPI, 'parse_request')
    def test_stat_config_maps(self, mock_parse_request, *args):
        mock_parse_request.return_value = ({}, {})

        config_map_servicer = ConfigMap()
        stat_info = config_map_servicer.stat({}, {})

        print_message(stat_info, 'test_stat_config_maps')


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
