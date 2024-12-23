import logging
from typing import Union

from spaceone.core.service import *

from spaceone.config.manager.domain_config_manager import DomainConfigManager
from spaceone.config.model.domain_config.request import *
from spaceone.config.model.domain_config.response import *
from spaceone.config.model.domain_config.database import DomainConfig

_LOGGER = logging.getLogger(__name__)


@authentication_handler
@authorization_handler
@mutation_handler
@event_handler
class DomainConfigService(BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.domain_config_mgr = DomainConfigManager()

    @transaction(permission="config:DomainConfig.write", role_types=["DOMAIN_ADMIN"])
    @convert_model
    def create(self, params: DomainConfigCreateRequest) -> Union[DomainConfigResponse, dict]:
        """Create domain config

        Args:
            params (DomainConfigCreateRequest): {
                'name': 'str',               # required
                'data': 'dict',              # required
                'tags': 'dict',
                'domain_id': 'str',          # injected from auth (required)
            }

        Returns:
            DomainConfigResponse:
        """

        domain_config_vo = self.domain_config_mgr.create_domain_config(params.dict())
        return DomainConfigResponse(**domain_config_vo.to_dict())

    @transaction(permission="config:DomainConfig.write", role_types=["DOMAIN_ADMIN"])
    @convert_model
    def update(self, params: DomainConfigUpdateRequest) -> Union[DomainConfigResponse, dict]:
        """Update domain config

        Args:
            params (DomainConfigUpdateRequest): {
                'name': 'str',          # required
                'data': 'dict',
                'tags': 'dict',
                'domain_id': 'str',     # injected from auth (required)
            }

        Returns:
            DomainConfigResponse:
        """

        domain_config_vo: DomainConfig = self.domain_config_mgr.get_domain_config(
            params.name, params.domain_id
        )

        domain_config_vo = self.domain_config_mgr.update_domain_config_by_vo(
            params.dict(exclude_unset=True), domain_config_vo
        )

        return DomainConfigResponse(**domain_config_vo.to_dict())

    @transaction(permission="config:DomainConfig.write", role_types=["DOMAIN_ADMIN"])
    @convert_model
    def set(self, params: DomainConfigSetRequest) -> Union[DomainConfigResponse, dict]:
        """Set domain config (create or update)

        Args:
            params (dict): {
                'name': 'str',          # required
                'data': 'dict',         # required
                'tags': 'dict',
                'domain_id': 'str',     # injected from auth (required)
            }

        Returns:
            DomainConfigResponse:
        """

        domain_config_vos = self.domain_config_mgr.filter_domain_configs(
            name=params.name, domain_id=params.domain_id
        )

        if domain_config_vos.count() == 0:
            domain_config_vo = self.domain_config_mgr.create_domain_config(params.dict())
        else:
            domain_config_vo = self.domain_config_mgr.update_domain_config_by_vo(
                params.dict(exclude_unset=True), domain_config_vos[0]
            )

        return DomainConfigResponse(**domain_config_vo.to_dict())

    @transaction(permission="config:DomainConfig.write", role_types=["DOMAIN_ADMIN"])
    @convert_model
    def delete(self, params: DomainConfigDeleteRequest) -> None:
        """Delete domain config

        Args:
            params (dict): {
                'name': 'str',          # required
                'domain_id': 'str'      # injected from auth (required)
            }

        Returns:
            None
        """

        domain_config_vo: DomainConfig = self.domain_config_mgr.get_domain_config(
            params.name, params.domain_id
        )

        self.domain_config_mgr.delete_domain_config_by_vo(domain_config_vo)

    @transaction(permission="config:DomainConfig.read", role_types=["DOMAIN_ADMIN"])
    @convert_model
    def get(self, params: DomainConfigGetRequest) -> Union[DomainConfigResponse, dict]:
        """Get domain config

        Args:
            params (dict): {
                'name': 'str',                # required
                'domain_id': 'str',           # injected from auth (required)
            }

        Returns:
            DomainConfigResponse:
        """

        domain_config_vo: DomainConfig = self.domain_config_mgr.get_domain_config(
            params.name, params.domain_id
        )

        return DomainConfigResponse(**domain_config_vo.to_dict())

    @transaction(permission="config:DomainConfig.read", role_types=["DOMAIN_ADMIN"])
    @append_query_filter(["name", "domain_id"])
    @append_keyword_filter(["name"])
    @convert_model
    def list(self, params: DomainConfigSearchQueryRequest) -> Union[DomainConfigsResponse, dict]:
        """List domain configs

        Args:
            params (dict): {
                'query': 'dict (spaceone.api.core.v1.Query)',
                'name': 'str',
                'domain_id': 'str'                  # injected from auth (required)
            }

        Returns:
            DomainConfigsResponse:
        """

        query = params.query or {}
        domain_configs_vos, total_count = self.domain_config_mgr.list_domain_configs(query)
        domain_configs_info = [
            domain_config_vo.to_dict() for domain_config_vo in domain_configs_vos
        ]
        return DomainConfigsResponse(results=domain_configs_info, total_count=total_count)
