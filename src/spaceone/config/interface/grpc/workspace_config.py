from spaceone.api.config.v1 import workspace_config_pb2, workspace_config_pb2_grpc
from spaceone.core.pygrpc import BaseAPI

from spaceone.config.service.workspace_config_service import WorkspaceConfigService
from spaceone.config.info.domain_config_info import *
from spaceone.config.info.common_info import *


class WorkspaceConfig(BaseAPI, workspace_config_pb2_grpc.WorkspaceConfigServicer):
    pb2 = workspace_config_pb2
    pb2_grpc = workspace_config_pb2_grpc

    def create(self, request, context):
        params, metadata = self.parse_request(request, context)
        workspace_config_svc = WorkspaceConfigService(metadata)
        response: dict = workspace_config_svc.create(params)
        return self.dict_to_message(response)

    def update(self, request, context):
        params, metadata = self.parse_request(request, context)
        workspace_config_svc = WorkspaceConfigService(metadata)
        response: dict = workspace_config_svc.update(params)
        return self.dict_to_message(response)

    def set(self, request, context):
        params, metadata = self.parse_request(request, context)
        workspace_config_svc = WorkspaceConfigService(metadata)
        response: dict = workspace_config_svc.set(params)
        return self.dict_to_message(response)

    def delete(self, request, context):
        params, metadata = self.parse_request(request, context)
        workspace_config_svc = WorkspaceConfigService(metadata)
        workspace_config_svc.delete(params)
        return self.empty()

    def get(self, request, context):
        params, metadata = self.parse_request(request, context)
        workspace_config_svc = WorkspaceConfigService(metadata)
        response: dict = workspace_config_svc.get(params)
        return self.dict_to_message(response)

    def list(self, request, context):
        params, metadata = self.parse_request(request, context)
        workspace_config_svc = WorkspaceConfigService(metadata)
        response: dict = workspace_config_svc.list(params)
        return self.dict_to_message(response)

    def stat(self, request, context):
        params, metadata = self.parse_request(request, context)
        workspace_config_svc = WorkspaceConfigService(metadata)
        response: dict = workspace_config_svc.stat(params)
        return self.dict_to_message(response)
