import logging
from typing import Union

from spaceone.core.service import *

from spaceone.config.manager.user_config_manager import UserConfigManager
from spaceone.config.model.user_config.request import *
from spaceone.config.model.user_config.response import *
from spaceone.config.model.user_config.database import UserConfig

_LOGGER = logging.getLogger(__name__)


@authentication_handler
@authorization_handler
@mutation_handler
@event_handler
class UserConfigService(BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_config_mgr = UserConfigManager()

    @transaction(permission="config:UserConfig.write", role_types=["USER"])
    @convert_model
    def create(self, params: UserConfigCreateRequest) -> Union[UserConfigResponse, dict]:
        """Create user config

        Args:
            params (UserConfigCreateRequest): {
                'name': 'str',               # required
                'data': 'dict',              # required
                'tags': 'dict',
                'domain_id': 'str',          # injected from auth (required)
                'user_id': 'str',            # injected from auth (required)
            }

        Returns:
            UserConfigResponse:
        """

        user_config_vo = self.user_config_mgr.create_user_config(params.dict())
        return UserConfigResponse(**user_config_vo.to_dict())

    @transaction(permission="config:UserConfig.write", role_types=["USER"])
    @convert_model
    def update(self, params: UserConfigUpdateRequest) -> Union[UserConfigResponse, dict]:
        """Update user config

        Args:
            params (UserConfigUpdateRequest): {
                'name': 'str',          # required
                'data': 'dict',
                'tags': 'dict',
                'domain_id': 'str',     # injected from auth (required)
                'user_id': 'str',       # injected from auth (required)
            }

        Returns:
            UserConfigResponse:
        """

        user_config_vo: UserConfig = self.user_config_mgr.get_user_config(
            params.name, params.domain_id, params.user_id
        )

        user_config_vo = self.user_config_mgr.update_user_config_by_vo(
            params.dict(exclude_unset=True), user_config_vo
        )

        return UserConfigResponse(**user_config_vo.to_dict())

    @transaction(permission="config:UserConfig.write", role_types=["USER"])
    @convert_model
    def set(self, params: UserConfigSetRequest) -> Union[UserConfigResponse, dict]:
        """Set user config (create or update)

        Args:
            params (dict): {
                'name': 'str',          # required
                'data': 'dict',         # required
                'tags': 'dict',
                'domain_id': 'str',     # injected from auth (required)
                'user_id': 'str',       # injected from auth (required)
            }

        Returns:
            UserConfigResponse:
        """

        user_config_vos = self.user_config_mgr.filter_user_configs(
            name=params.name, domain_id=params.domain_id, user_id=params.user_id
        )

        if user_config_vos.count() == 0:
            user_config_vo = self.user_config_mgr.create_user_config(params.dict())
        else:
            user_config_vo = self.user_config_mgr.update_user_config_by_vo(
                params.dict(exclude_unset=True), user_config_vos[0]
            )

        return UserConfigResponse(**user_config_vo.to_dict())

    @transaction(permission="config:UserConfig.write", role_types=["USER"])
    @convert_model
    def delete(self, params: UserConfigDeleteRequest) -> None:
        """Delete user config

        Args:
            params (dict): {
                'name': 'str',          # required
                'domain_id': 'str'      # injected from auth (required)
                'user_id': 'str',       # injected from auth (required)
            }

        Returns:
            None
        """

        user_config_vo: UserConfig = self.user_config_mgr.get_user_config(
            params.name, params.domain_id, params.user_id
        )

        self.user_config_mgr.delete_user_config_by_vo(user_config_vo)

    @transaction(permission="config:UserConfig.read", role_types=["USER"])
    @convert_model
    def get(self, params: UserConfigGetRequest) -> Union[UserConfigResponse, dict]:
        """Get user config

        Args:
            params (dict): {
                'name': 'str',                # required
                'domain_id': 'str',           # injected from auth (required)
                'user_id': 'str',             # injected from auth (required)
            }

        Returns:
            UserConfigResponse:
        """

        user_config_vo: UserConfig = self.user_config_mgr.get_user_config(
            params.name, params.domain_id, params.user_id
        )

        return UserConfigResponse(**user_config_vo.to_dict())

    @transaction(permission="config:UserConfig.read", role_types=["USER"])
    @append_query_filter(["name", "domain_id", "user_id"])
    @append_keyword_filter(["name"])
    @convert_model
    def list(self, params: UserConfigSearchQueryRequest) -> Union[UserConfigsResponse, dict]:
        """List user configs

        Args:
            params (dict): {
                'query': 'dict (spaceone.api.core.v1.Query)',
                'name': 'str',
                'domain_id': 'str'                  # injected from auth (required)
                'user_id': 'str',                   # injected from auth (required)
            }

        Returns:
            UserConfigsResponse:
        """

        query = params.query or {}
        user_configs_vos, total_count = self.user_config_mgr.list_user_configs(query)
        user_configs_info = [
            user_config_vo.to_dict() for user_config_vo in user_configs_vos
        ]
        return UserConfigsResponse(results=user_configs_info, total_count=total_count)
