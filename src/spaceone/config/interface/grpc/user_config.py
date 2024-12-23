from spaceone.api.config.v1 import user_config_pb2, user_config_pb2_grpc
from spaceone.core.pygrpc import BaseAPI

from spaceone.config.service.user_config_service import UserConfigService


class UserConfig(BaseAPI, user_config_pb2_grpc.UserConfigServicer):
    pb2 = user_config_pb2
    pb2_grpc = user_config_pb2_grpc

    def create(self, request, context):
        params, metadata = self.parse_request(request, context)
        user_config_svc = UserConfigService(metadata)
        response: dict = user_config_svc.create(params)
        return self.dict_to_message(response)

    def update(self, request, context):
        params, metadata = self.parse_request(request, context)
        user_config_svc = UserConfigService(metadata)
        response: dict = user_config_svc.update(params)
        return self.dict_to_message(response)

    def set(self, request, context):
        params, metadata = self.parse_request(request, context)
        user_config_svc = UserConfigService(metadata)
        response: dict = user_config_svc.set(params)
        return self.dict_to_message(response)

    def delete(self, request, context):
        params, metadata = self.parse_request(request, context)
        user_config_svc = UserConfigService(metadata)
        user_config_svc.delete(params)
        return self.empty()

    def get(self, request, context):
        params, metadata = self.parse_request(request, context)
        user_config_svc = UserConfigService(metadata)
        response: dict = user_config_svc.get(params)
        return self.dict_to_message(response)

    def list(self, request, context):
        params, metadata = self.parse_request(request, context)
        user_config_svc = UserConfigService(metadata)
        response: dict = user_config_svc.list(params)
        return self.dict_to_message(response)
