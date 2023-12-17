import logging

from spaceone.core.service import *

from spaceone.config.manager.user_config_manager import UserConfigManager
from spaceone.config.model import UserConfig

_LOGGER = logging.getLogger(__name__)


@authentication_handler
@authorization_handler
@mutation_handler
@event_handler
class UserConfigService(BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_config_mgr: UserConfigManager = self.locator.get_manager(
            "UserConfigManager"
        )

    @transaction(permission="config:UserConfig.write", role_types=["USER"])
    @check_required(["name", "data", "user_id", "domain_id"])
    def create(self, params: dict) -> UserConfig:
        """Create user config

        Args:
            params (dict): {
                'name': 'str',               # required
                'data': 'dict',              # required
                'tags': 'dict',
                'user_id': 'str'(meta)       # injected from auth
                'domain_id': 'str'(meta),    # injected from auth
            }

        Returns:
            user_config_vo (object)
        """

        return self.user_config_mgr.create_user_config(params)

    @transaction(permission="config:UserConfig.write", role_types=["USER"])
    @check_required(["name", "user_id", "domain_id"])
    def update(self, params: dict) -> UserConfig:
        """Update user config

        Args:
            params (dict): {
                'name': 'str',        # required
                'data': 'dict',
                'tags': 'dict',
                'domain_id': 'str'    # injected from auth
                'user_id': 'str'      # injected from auth
            }

        Returns:
            user_config_vo (object)
        """

        return self.user_config_mgr.update_user_config(params)

    @transaction(permission="config:UserConfig.write", role_types=["USER"])
    @check_required(["name", "data", "user_id", "domain_id"])
    def set(self, params: dict) -> UserConfig:
        """Set user config (create or update)

        Args:
            params (dict): {
                'name': 'str',         # required
                'data': 'dict',        # required
                'tags': 'dict',
                'user_id': 'str'       # injected from auth
                'domain_id': 'str'     # injected from auth
            }

        Returns:
            user_config_vo (object)
        """

        user_config_vos = self.user_config_mgr.filter_user_configs(
            name=params["name"],
            user_id=params["user_id"],
            domain_id=params["domain_id"],
        )

        if user_config_vos.count() == 0:
            return self.user_config_mgr.create_user_config(params)
        else:
            return self.user_config_mgr.update_user_config_by_vo(
                params, user_config_vos[0]
            )

    @transaction(permission="config:UserConfig.write", role_types=["USER"])
    @check_required(["name", "user_id", "domain_id"])
    def delete(self, params):
        """Delete user config

        Args:
            params (dict): {
                'name': 'str',          # required
                'user_id': 'str',       # injected from auth
                'domain_id': 'str'      # injected from auth
            }

        Returns:
            None
        """

        self.user_config_mgr.delete_user_config(
            params["name"], params["user_id"], params["domain_id"]
        )

    @transaction(permission="config:UserConfig.read", role_types=["USER"])
    @check_required(["name", "user_id", "domain_id"])
    def get(self, params):
        """Get user config

        Args:
            params (dict): {
                'name': 'str',                # required
                'domain_id': 'str',(meta),    # required
                'user_id': 'str'(meta)        # required
            }

        Returns:
            user_config_vo (object)
        """

        return self.user_config_mgr.get_user_config(
            params["name"], params["user_id"], params["domain_id"]
        )

    @transaction(permission="config:UserConfig.read", role_types=["USER"])
    @check_required(["user_id", "domain_id"])
    @append_query_filter(["name", "user_id", "domain_id"])
    @append_keyword_filter(["name"])
    def list(self, params: dict) -> dict:
        """List user configs

        Args:
            params (dict): {
                'query': 'dict (spaceone.api.core.v1.Query)',
                'name': 'str',
                'user_id': 'str',                               # injected from auth
                'domain_id': 'str'                              # injected from auth
            }

        Returns:
            user_config_vos (objects)
            total_count (int)
        """

        query = params.get("query", {})
        return self.user_config_mgr.list_user_configs(query)

    @transaction(permission="config:UserConfig.read", role_types=["USER"])
    @check_required(["query", "domain_id", "user_id"])
    @append_query_filter(["domain_id", "user_id"])
    @append_keyword_filter(["name"])
    def stat(self, params):
        """
        Args:
            params (dict): {
                'query': 'dict (spaceone.api.core.v1.StatisticsQuery)',    # required
                'user_id': 'str'(meta)                                     # injected from auth
                'domain_id': 'str'(meta),                                  # injected from auth
            }

        Returns:
            values (list) : 'list of statistics data'

        """

        query = params.get("query", {})
        return self.user_config_mgr.state_user_configs(query)
