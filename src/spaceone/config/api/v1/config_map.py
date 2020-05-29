from spaceone.api.config.v1 import config_map_pb2, config_map_pb2_grpc
from spaceone.core.pygrpc import BaseAPI


class ConfigMap(BaseAPI, config_map_pb2_grpc.ConfigMapServicer):

    pb2 = config_map_pb2
    pb2_grpc = config_map_pb2_grpc

    def create(self, request, context):
        params, metadata = self.parse_request(request, context)

        with self.locator.get_service('ConfigMapService', metadata) as config_map_service:
            return self.locator.get_info('ConfigMapInfo', config_map_service.create(params))

    def update(self, request, context):
        params, metadata = self.parse_request(request, context)

        with self.locator.get_service('ConfigMapService', metadata) as config_map_service:
            return self.locator.get_info('ConfigMapInfo', config_map_service.update(params))

    def delete(self, request, context):
        params, metadata = self.parse_request(request, context)

        with self.locator.get_service('ConfigMapService', metadata) as config_map_service:
            config_map_service.delete(params)
            return self.locator.get_info('EmptyInfo')

    def get(self, request, context):
        params, metadata = self.parse_request(request, context)

        with self.locator.get_service('ConfigMapService', metadata) as config_map_service:
            return self.locator.get_info('ConfigMapInfo', config_map_service.get(params))

    def list(self, request, context):
        params, metadata = self.parse_request(request, context)

        with self.locator.get_service('ConfigMapService', metadata) as config_map_service:
            config_map_vos, total_count = config_map_service.list(params)
            return self.locator.get_info('ConfigMapsInfo', config_map_vos,
                                         total_count, minimal=self.get_minimal(params))

    def stat(self, request, context):
        params, metadata = self.parse_request(request, context)

        with self.locator.get_service('ConfigMapService', metadata) as config_map_service:
            return self.locator.get_info('StatisticsInfo', config_map_service.stat(params))
