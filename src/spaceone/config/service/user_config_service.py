import logging

from spaceone.core.error import *
from spaceone.core.service import *

from spaceone.config.manager.user_config_manager import UserConfigManager

_LOGGER = logging.getLogger(__name__)


@authentication_handler
@authorization_handler
@mutation_handler
@event_handler
class UserConfigService(BaseService):
    service = "config"
    resource = "UserConfig"
    permission_group = "USER"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_config_mgr: UserConfigManager = self.locator.get_manager(
            "UserConfigManager"
        )

    @transaction(scope="user:write")
    @check_required(["name", "data", "domain_id", "user_id"])
    def create(self, params):
        """Create user config

        Args:
            params (dict): {
                'name': 'str',               # required
                'data': 'dict',              # required
                'tags': 'dict',
                'domain_id': 'str'(meta),    # required
                'user_id': 'str'(meta)       # required
            }

        Returns:
            user_config_vo (object)
        """

        self._check_permission(params["domain_id"])

        params["user_id"] = self.transaction.get_meta("user_id")

        return self.user_config_mgr.create_user_config(params)

    @transaction(scope="user:write")
    @check_required(["name", "domain_id", "user_id"])
    def update(self, params):
        """Update user config

        Args:
            params (dict): {
                'name': 'str',              # required
                'data': 'dict',
                'tags': 'dict',
                'domain_id': 'str'(meta)    # required
                'user_id': 'str'(meta)      # required
            }

        Returns:
            user_config_vo (object)
        """

        self._check_permission(params["domain_id"])

        params["user_id"] = self.transaction.get_meta("user_id")

        return self.user_config_mgr.update_user_config(params)

    @transaction(scope="user:write")
    @check_required(["name", "data", "domain_id", "user_id"])
    def set(self, params):
        """Set user config (create or update)

        Args:
            params (dict): {
                'name': 'str',               # required
                'data': 'dict',              # required
                'tags': 'dict',
                'domain_id': 'str'(meta),    # required
                'user_id': 'str'(meta)       # required
            }

        Returns:
            user_config_vo (object)
        """

        self._check_permission(params["domain_id"])

        params["user_id"] = self.transaction.get_meta("user_id")

        user_type = self.transaction.get_meta("authorization.user_type")
        if user_type == "DOMAIN_OWNER":
            raise ERROR_PERMISSION_DENIED()

        user_config_vos = self.user_config_mgr.filter_user_configs(
            domain_id=params["domain_id"],
            user_id=params["user_id"],
            name=params["name"],
        )

        if user_config_vos.count() == 0:
            return self.user_config_mgr.create_user_config(params)
        else:
            return self.user_config_mgr.update_user_config_by_vo(
                params, user_config_vos[0]
            )

    @transaction(scope="user:write")
    @check_required(["name", "domain_id", "user_id"])
    def delete(self, params):
        """Delete user config

        Args:
            params (dict): {
                'name': 'str',               # required
                'domain_id': 'str'(meta),    # required
                'user_id': 'str'(meta)       # required
            }

        Returns:
            None
        """

        self._check_permission(params["domain_id"])
        user_id = self.transaction.get_meta("user_id")

        self.user_config_mgr.delete_user_config(
            params["name"], user_id, params["domain_id"]
        )

    @transaction(scope="user:read")
    @check_required(["name", "domain_id", "user_id"])
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

        user_id = self.transaction.get_meta("user_id")

        return self.user_config_mgr.get_user_config(
            params["name"], user_id, params["domain_id"], params.get("only")
        )

    @transaction(scope="user:read")
    @check_required(["domain_id"])
    @append_query_filter(["name", "user_id", "domain_id"])
    @append_keyword_filter(["name"])
    def list(self, params):
        """List user configs

        Args:
            params (dict): {
                'query': 'dict (spaceone.api.core.v1.Query)',
                'name': 'str',
                'domain_id': 'str'(meta),                        # required
                'user_id': 'str'(meta)                           # required
            }

        Returns:
            user_config_vos (objects)
            total_count (int)
        """

        query = params.get("query", {})
        return self.user_config_mgr.list_user_configs(query)

    @transaction(scope="user:read")
    @check_required(["query", "domain_id", "user_id"])
    @append_query_filter(["domain_id", "user_id"])
    @append_keyword_filter(["name"])
    def stat(self, params):
        """
        Args:
            params (dict): {
                'query': 'dict (spaceone.api.core.v1.StatisticsQuery)',    # required
                'domain_id': 'str'(meta),                                  # required
                'user_id': 'str'(meta)                                     # required
            }

        Returns:
            values (list) : 'list of statistics data'

        """

        query = params.get("query", {})
        return self.user_config_mgr.state_user_configs(query)

    def _check_permission(self, request_domain_id):
        user_type = self.transaction.get_meta("authorization.user_type")
        user_domain_id = self.transaction.get_meta("domain_id")

        if user_type == "DOMAIN_OWNER" or request_domain_id != user_domain_id:
            raise ERROR_PERMISSION_DENIED()
