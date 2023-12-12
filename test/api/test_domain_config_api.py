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
from spaceone.api.config.v1 import domain_config_pb2
from spaceone.config.interface.grpc.domain_config import DomainConfig
from test.factory.domain_config_factory import DomainConfigFactory


class _MockDomainConfigService(BaseService):
    def create(self, params):
        params = copy.deepcopy(params)

        return DomainConfigFactory(**params)

    def update(self, params):
        params = copy.deepcopy(params)

        return DomainConfigFactory(**params)

    def set(self, params):
        params = copy.deepcopy(params)

        return DomainConfigFactory(**params)

    def delete(self, params):
        pass

    def get(self, params):
        return DomainConfigFactory(**params)

    def list(self, params):
        return DomainConfigFactory.build_batch(10, **params), 10

    def stat(self, params):
        return {"result": [{"name": utils.random_string(), "config_count": 100}]}


class TestDomainConfigAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        config.init_conf(package="spaceone.config")
        connect("test", host="mongomock://localhost")
        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        disconnect()

    @patch.object(BaseAPI, "__init__", return_value=None)
    @patch.object(Locator, "get_service", return_value=_MockDomainConfigService())
    @patch.object(BaseAPI, "parse_request")
    def test_create_domain_config(self, mock_parse_request, *args):
        params = {
            "name": utils.random_string(),
            "data": {"config_key": "config_value"},
            "tags": {utils.random_string(): utils.random_string()},
            "domain_id": utils.generate_id("domain"),
        }
        mock_parse_request.return_value = (params, {})

        domain_config_servicer = DomainConfig()
        domain_config_info = domain_config_servicer.create({}, {})

        print_message(domain_config_info, "test_create_domain_config")
        domain_config_data = MessageToDict(
            domain_config_info, preserving_proto_field_name=True
        )

        self.assertIsInstance(domain_config_info, domain_config_pb2.DomainConfigInfo)
        self.assertEqual(domain_config_info.name, params["name"])
        self.assertDictEqual(MessageToDict(domain_config_info.data), params["data"])
        self.assertDictEqual(domain_config_data["tags"], params["tags"])
        self.assertEqual(domain_config_info.domain_id, params["domain_id"])
        self.assertIsNotNone(getattr(domain_config_info, "created_at", None))
        self.assertIsNotNone(getattr(domain_config_info, "updated_at", None))

    @patch.object(BaseAPI, "__init__", return_value=None)
    @patch.object(Locator, "get_service", return_value=_MockDomainConfigService())
    @patch.object(BaseAPI, "parse_request")
    def test_update_domain_config(self, mock_parse_request, *args):
        params = {
            "name": utils.random_string(),
            "data": {"update_config_key": "update_config_value"},
            "tags": {"update_key": "update_value"},
            "domain_id": utils.generate_id("domain"),
        }
        mock_parse_request.return_value = (params, {})

        domain_config_servicer = DomainConfig()
        domain_config_info = domain_config_servicer.update({}, {})

        print_message(domain_config_info, "test_update_domain_config")
        domain_config_data = MessageToDict(
            domain_config_info, preserving_proto_field_name=True
        )

        self.assertIsInstance(domain_config_info, domain_config_pb2.DomainConfigInfo)
        self.assertDictEqual(MessageToDict(domain_config_info.data), params["data"])
        self.assertDictEqual(domain_config_data["tags"], params["tags"])

    @patch.object(BaseAPI, "__init__", return_value=None)
    @patch.object(Locator, "get_service", return_value=_MockDomainConfigService())
    @patch.object(BaseAPI, "parse_request")
    def test_set_domain_config(self, mock_parse_request, *args):
        params = {
            "name": utils.random_string(),
            "data": {"config_key": "config_value"},
            "tags": {utils.random_string(): utils.random_string()},
            "domain_id": utils.generate_id("domain"),
        }
        mock_parse_request.return_value = (params, {})

        domain_config_servicer = DomainConfig()
        domain_config_info = domain_config_servicer.set({}, {})

        print_message(domain_config_info, "test_set_domain_config")
        domain_config_data = MessageToDict(
            domain_config_info, preserving_proto_field_name=True
        )

        self.assertIsInstance(domain_config_info, domain_config_pb2.DomainConfigInfo)
        self.assertEqual(domain_config_info.name, params["name"])
        self.assertDictEqual(MessageToDict(domain_config_info.data), params["data"])
        self.assertDictEqual(domain_config_data["tags"], params["tags"])
        self.assertEqual(domain_config_info.domain_id, params["domain_id"])
        self.assertIsNotNone(getattr(domain_config_info, "created_at", None))
        self.assertIsNotNone(getattr(domain_config_info, "updated_at", None))

    @patch.object(BaseAPI, "__init__", return_value=None)
    @patch.object(Locator, "get_service", return_value=_MockDomainConfigService())
    @patch.object(BaseAPI, "parse_request")
    def test_delete_domain_config(self, mock_parse_request, *args):
        mock_parse_request.return_value = ({}, {})

        domain_config_servicer = DomainConfig()
        result = domain_config_servicer.delete({}, {})

        print_message(result, "test_delete_domain_config")

        self.assertIsInstance(result, Empty)

    @patch.object(BaseAPI, "__init__", return_value=None)
    @patch.object(Locator, "get_service", return_value=_MockDomainConfigService())
    @patch.object(BaseAPI, "parse_request")
    def test_get_domain_config(self, mock_parse_request, *args):
        mock_parse_request.return_value = ({}, {})

        domain_config_servicer = DomainConfig()
        domain_config_info = domain_config_servicer.get({}, {})

        print_message(domain_config_info, "test_get_domain_config")

        self.assertIsInstance(domain_config_info, domain_config_pb2.DomainConfigInfo)

    @patch.object(BaseAPI, "__init__", return_value=None)
    @patch.object(Locator, "get_service", return_value=_MockDomainConfigService())
    @patch.object(BaseAPI, "parse_request")
    def test_list_domain_configs(self, mock_parse_request, *args):
        mock_parse_request.return_value = ({}, {})

        domain_config_servicer = DomainConfig()
        domain_configs_info = domain_config_servicer.list({}, {})

        print_message(domain_configs_info, "test_list_domain_configs")

        self.assertIsInstance(domain_configs_info, domain_config_pb2.DomainConfigsInfo)
        self.assertIsInstance(
            domain_configs_info.results[0], domain_config_pb2.DomainConfigInfo
        )
        self.assertEqual(domain_configs_info.total_count, 10)

    @patch.object(BaseAPI, "__init__", return_value=None)
    @patch.object(Locator, "get_service", return_value=_MockDomainConfigService())
    @patch.object(BaseAPI, "parse_request")
    def test_stat_domain_configs(self, mock_parse_request, *args):
        mock_parse_request.return_value = ({}, {})

        domain_config_servicer = DomainConfig()
        stat_info = domain_config_servicer.stat({}, {})
        print_message(stat_info, "test_stat_domain_configs")


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
