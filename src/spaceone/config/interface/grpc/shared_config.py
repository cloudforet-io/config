from spaceone.api.config.v1 import shared_config_pb2, shared_config_pb2_grpc
from spaceone.core.pygrpc import BaseAPI

from spaceone.config.service.shared_config_service import SharedConfigService


class SharedConfig(BaseAPI, shared_config_pb2_grpc.SharedConfigServicer):
    pb2 = shared_config_pb2
    pb2_grpc = shared_config_pb2_grpc

    def create(self, request, context):
        params, metadata = self.parse_request(request, context)
        shared_config_svc = SharedConfigService(metadata)
        response: dict = shared_config_svc.create(params)
        return self.dict_to_message(response)

    def update(self, request, context):
        params, metadata = self.parse_request(request, context)
        shared_config_svc = SharedConfigService(metadata)
        response: dict = shared_config_svc.update(params)
        return self.dict_to_message(response)

    def delete(self, request, context):
        params, metadata = self.parse_request(request, context)
        shared_config_svc = SharedConfigService(metadata)
        shared_config_svc.delete(params)
        return self.empty()

    def get(self, request, context):
        params, metadata = self.parse_request(request, context)
        shared_config_svc = SharedConfigService(metadata)
        response: dict = shared_config_svc.get(params)
        return self.dict_to_message(response)

    def list(self, request, context):
        params, metadata = self.parse_request(request, context)
        shared_config_svc = SharedConfigService(metadata)
        response: dict = shared_config_svc.list(params)
        return self.dict_to_message(response)
