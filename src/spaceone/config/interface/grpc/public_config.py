from spaceone.api.config.v1 import public_config_pb2, public_config_pb2_grpc
from spaceone.core.pygrpc import BaseAPI

from spaceone.config.service.public_config_service import PublicConfigService


class PublicConfig(BaseAPI, public_config_pb2_grpc.PublicConfigServicer):
    pb2 = public_config_pb2
    pb2_grpc = public_config_pb2_grpc

    def create(self, request, context):
        params, metadata = self.parse_request(request, context)
        public_config_svc = PublicConfigService(metadata)
        response: dict = public_config_svc.create(params)
        return self.dict_to_message(response)

    def update(self, request, context):
        params, metadata = self.parse_request(request, context)
        public_config_svc = PublicConfigService(metadata)
        response: dict = public_config_svc.update(params)
        return self.dict_to_message(response)

    def set(self, request, context):
        params, metadata = self.parse_request(request, context)
        public_config_svc = PublicConfigService(metadata)
        response: dict = public_config_svc.set(params)
        return self.dict_to_message(response)

    def delete(self, request, context):
        params, metadata = self.parse_request(request, context)
        public_config_svc = PublicConfigService(metadata)
        public_config_svc.delete(params)
        return self.empty()

    def get(self, request, context):
        params, metadata = self.parse_request(request, context)
        public_config_svc = PublicConfigService(metadata)
        response: dict = public_config_svc.get(params)
        return self.dict_to_message(response)

    def list(self, request, context):
        params, metadata = self.parse_request(request, context)
        public_config_svc = PublicConfigService(metadata)
        response: dict = public_config_svc.list(params)
        return self.dict_to_message(response)

    def stat(self, request, context):
        params, metadata = self.parse_request(request, context)
        public_config_svc = PublicConfigService(metadata)
        response: dict = public_config_svc.stat(params)
        return self.dict_to_message(response)
