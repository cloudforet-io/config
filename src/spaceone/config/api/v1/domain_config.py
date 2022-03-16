from spaceone.api.config.v1 import domain_config_pb2, domain_config_pb2_grpc
from spaceone.core.pygrpc import BaseAPI


class DomainConfig(BaseAPI, domain_config_pb2_grpc.DomainConfigServicer):

    pb2 = domain_config_pb2
    pb2_grpc = domain_config_pb2_grpc

    def create(self, request, context):
        params, metadata = self.parse_request(request, context)

        with self.locator.get_service('DomainConfigService', metadata) as domain_config_service:
            return self.locator.get_info('DomainConfigInfo', domain_config_service.create(params))

    def update(self, request, context):
        params, metadata = self.parse_request(request, context)

        with self.locator.get_service('DomainConfigService', metadata) as domain_config_service:
            return self.locator.get_info('DomainConfigInfo', domain_config_service.update(params))

    def set(self, request, context):
        params, metadata = self.parse_request(request, context)

        with self.locator.get_service('DomainConfigService', metadata) as domain_config_service:
            return self.locator.get_info('DomainConfigInfo', domain_config_service.set(params))

    def delete(self, request, context):
        params, metadata = self.parse_request(request, context)

        with self.locator.get_service('DomainConfigService', metadata) as domain_config_service:
            domain_config_service.delete(params)
            return self.locator.get_info('EmptyInfo')

    def get(self, request, context):
        params, metadata = self.parse_request(request, context)

        with self.locator.get_service('DomainConfigService', metadata) as domain_config_service:
            return self.locator.get_info('DomainConfigInfo', domain_config_service.get(params))

    def list(self, request, context):
        params, metadata = self.parse_request(request, context)

        with self.locator.get_service('DomainConfigService', metadata) as domain_config_service:
            domain_config_vos, total_count = domain_config_service.list(params)
            return self.locator.get_info('DomainConfigsInfo', domain_config_vos,
                                         total_count, minimal=self.get_minimal(params))

    def stat(self, request, context):
        params, metadata = self.parse_request(request, context)

        with self.locator.get_service('DomainConfigService', metadata) as domain_config_service:
            return self.locator.get_info('StatisticsInfo', domain_config_service.stat(params))
