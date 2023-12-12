import logging

from spaceone.core.service import *

from spaceone.config.manager.domain_config_manager import DomainConfigManager

_LOGGER = logging.getLogger(__name__)


@authentication_handler
@authorization_handler
@mutation_handler
@event_handler
class DomainConfigService(BaseService):
    service = "config"
    resource = "DomainConfig"
    permission_group = "DOMAIN"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.domain_config_mgr: DomainConfigManager = self.locator.get_manager(
            DomainConfigManager
        )

    @transaction(scope="domain_admin:write")
    @check_required(["name", "data", "domain_id"])
    def create(self, params):
        """Create domain config

        Args:
            params (dict): {
                'name': 'str',        # required
                'data': 'dict',       # required
                'tags': 'dict',
                'domain_id': 'str'    # required
            }

        Returns:
            domain_config_vo (object)
        """

        return self.domain_config_mgr.create_domain_config(params)

    @transaction(scope="domain_admin:write")
    @check_required(["name", "domain_id"])
    def update(self, params):
        """Update domain config

        Args:
            params (dict): {
                'name': 'str',        # required
                'data': 'dict',
                'tags': 'dict',
                'domain_id': 'str'    # required
            }

        Returns:
            domain_config_vo (object)
        """

        return self.domain_config_mgr.update_domain_config(params)

    @transaction(scope="domain_admin:write")
    @check_required(["name", "data", "domain_id"])
    def set(self, params):
        """Set domain config (create or update)

        Args:
            params (dict): {
                'name': 'str',        # required
                'data': 'dict',       # required
                'tags': 'dict',
                'domain_id': 'str'    # required
            }

        Returns:
            domain_config_vo (object)
        """

        domain_id = params["domain_id"]

        domain_config_vos = self.domain_config_mgr.filter_domain_configs(
            domain_id=domain_id, name=params["name"]
        )

        if domain_config_vos.count() == 0:
            return self.domain_config_mgr.create_domain_config(params)
        else:
            return self.domain_config_mgr.update_domain_config_by_vo(
                params, domain_config_vos[0]
            )

    @transaction(scope="domain_admin:write")
    @check_required(["name", "domain_id"])
    def delete(self, params):
        """Delete domain config

        Args:
            params (dict): {
                'name': 'str',        # required
                'domain_id': 'str'    # required
            }

        Returns:
            None
        """

        self.domain_config_mgr.delete_domain_config(params["name"], params["domain_id"])

    @transaction(scope="domain_admin:read")
    @check_required(["name", "domain_id"])
    def get(self, params):
        """Get domain config

        Args:
            params (dict): {
                'name': 'str',        # required
                'domain_id': 'str'    # required
            }

        Returns:
            domain_config_vo (object)
        """

        return self.domain_config_mgr.get_domain_config(
            params["name"], params["domain_id"], params.get("only")
        )

    @transaction(scope="domain_admin:read")
    @check_required(["domain_id"])
    @append_query_filter(["name", "domain_id"])
    @append_keyword_filter(["name"])
    def list(self, params):
        """List domain configs

        Args:
            params (dict): {
                'query': 'dict (spaceone.api.core.v1.Query)'
                'name': 'str',
                'domain_id': 'str',                             # required
            }

        Returns:
            domain_config_vos (objects)
            total_count (int)
        """

        query = params.get("query", {})
        return self.domain_config_mgr.list_domain_configs(query)

    @transaction(scope="domain_admin:read")
    @check_required(["query", "domain_id"])
    @append_query_filter(["domain_id"])
    @append_keyword_filter(["name"])
    def stat(self, params):
        """
        Args:
            params (dict): {
                'query': 'dict (spaceone.api.core.v1.StatisticsQuery)'    # required
                'domain_id': 'str',                                       # required
            }

        Returns:
            values (list) : 'list of statistics data'

        """

        query = params.get("query", {})
        return self.domain_config_mgr.state_domain_configs(query)
