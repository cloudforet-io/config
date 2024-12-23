import logging
from typing import Union

from spaceone.core.service import *

from spaceone.config.manager.public_config_manager import PublicConfigManager
from spaceone.config.model.public_config.request import *
from spaceone.config.model.public_config.response import *
from spaceone.config.model.public_config.database import PublicConfig

_LOGGER = logging.getLogger(__name__)


@authentication_handler
@authorization_handler
@mutation_handler
@event_handler
class PublicConfigService(BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.public_config_mgr = PublicConfigManager()

    @transaction(permission="config:PublicConfig.write", role_types=["DOMAIN_ADMIN"])
    @convert_model
    def create(self, params: PublicConfigCreateRequest) -> Union[PublicConfigResponse, dict]:
        """Create public config

        Args:
            params (PublicConfigCreateRequest): {
                'name': 'str',               # required
                'data': 'dict',              # required
                'tags': 'dict',
                'domain_id': 'str',          # injected from auth (required)
            }

        Returns:
            PublicConfigResponse:
        """

        public_config_vo = self.public_config_mgr.create_public_config(params.dict())
        return PublicConfigResponse(**public_config_vo.to_dict())

    @transaction(permission="config:PublicConfig.write", role_types=["DOMAIN_ADMIN"])
    @convert_model
    def update(self, params: PublicConfigUpdateRequest) -> Union[PublicConfigResponse, dict]:
        """Update public config

        Args:
            params (PublicConfigUpdateRequest): {
                'name': 'str',          # required
                'data': 'dict',
                'tags': 'dict',
                'domain_id': 'str',     # injected from auth (required)
            }

        Returns:
            PublicConfigResponse:
        """

        public_config_vo: PublicConfig = self.public_config_mgr.get_public_config(
            params.name, params.domain_id
        )

        public_config_vo = self.public_config_mgr.update_public_config_by_vo(
            params.dict(exclude_unset=True), public_config_vo
        )

        return PublicConfigResponse(**public_config_vo.to_dict())

    @transaction(permission="config:PublicConfig.write", role_types=["DOMAIN_ADMIN"])
    @convert_model
    def set(self, params: PublicConfigSetRequest) -> Union[PublicConfigResponse, dict]:
        """Set public config (create or update)

        Args:
            params (dict): {
                'name': 'str',          # required
                'data': 'dict',         # required
                'tags': 'dict',
                'domain_id': 'str',     # injected from auth (required)
            }

        Returns:
            PublicConfigResponse:
        """

        public_config_vos = self.public_config_mgr.filter_public_configs(
            name=params.name, domain_id=params.domain_id
        )

        if public_config_vos.count() == 0:
            public_config_vo = self.public_config_mgr.create_public_config(params.dict())
        else:
            public_config_vo = self.public_config_mgr.update_public_config_by_vo(
                params.dict(exclude_unset=True), public_config_vos[0]
            )

        return PublicConfigResponse(**public_config_vo.to_dict())

    @transaction(permission="config:PublicConfig.write", role_types=["DOMAIN_ADMIN"])
    @convert_model
    def delete(self, params: PublicConfigDeleteRequest) -> None:
        """Delete public config

        Args:
            params (dict): {
                'name': 'str',          # required
                'domain_id': 'str'      # injected from auth (required)
            }

        Returns:
            None
        """

        public_config_vo: PublicConfig = self.public_config_mgr.get_public_config(
            params.name, params.domain_id
        )

        self.public_config_mgr.delete_public_config_by_vo(public_config_vo)

    @transaction(exclude=["authentication", "authorization", "mutation"])
    @convert_model
    def get(self, params: PublicConfigGetRequest) -> Union[PublicConfigResponse, dict]:
        """Get public config

        Args:
            params (dict): {
                'name': 'str',                # required
                'domain_id': 'str',           # injected from auth (required)
            }

        Returns:
            PublicConfigResponse:
        """

        public_config_vo: PublicConfig = self.public_config_mgr.get_public_config(
            params.name, params.domain_id
        )

        return PublicConfigResponse(**public_config_vo.to_dict())

    @transaction(exclude=["authentication", "authorization", "mutation"])
    @append_query_filter(["name", "domain_id"])
    @append_keyword_filter(["name"])
    @convert_model
    def list(self, params: PublicConfigSearchQueryRequest) -> Union[PublicConfigsResponse, dict]:
        """List public configs

        Args:
            params (dict): {
                'query': 'dict (spaceone.api.core.v1.Query)',
                'name': 'str',
                'domain_id': 'str'                  # injected from auth (required)
            }

        Returns:
            PublicConfigsResponse:
        """

        query = params.query or {}
        public_configs_vos, total_count = self.public_config_mgr.list_public_configs(query)
        public_configs_info = [
            public_config_vo.to_dict() for public_config_vo in public_configs_vos
        ]
        return PublicConfigsResponse(results=public_configs_info, total_count=total_count)
