import logging
import copy

from spaceone.core.service import *
from spaceone.config.manager.config_map_manager import ConfigMapManager

_LOGGER = logging.getLogger(__name__)


@authentication_handler
@authorization_handler
@event_handler
class ConfigMapService(BaseService):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_map_mgr: ConfigMapManager = self.locator.get_manager('ConfigMapManager')

    @transaction
    @check_required(['name', 'data', 'domain_id'])
    def create(self, params):
        """Create config map

        Args:
            params (dict): {
                'name': 'str',
                'data': 'dict',
                'tags': 'dict',
                'domain_id': 'str'
            }

        Returns:
            config_map_vo (object)
        """

        return self.config_map_mgr.create_config_map(params)

    @transaction
    @check_required(['name', 'domain_id'])
    def update(self, params):
        """Update config map

        Args:
            params (dict): {
                'name': 'str',
                'data': 'dict',
                'tags': 'dict',
                'domain_id': 'str'
            }

        Returns:
            config_map_vo (object)
        """
        return self.config_map_mgr.update_config_map(params)

    @transaction
    @check_required(['name', 'domain_id'])
    def delete(self, params):
        """Delete config map

        Args:
            params (dict): {
                'name': 'str',
                'domain_id': 'str'
            }

        Returns:
            None
        """

        self.config_map_mgr.delete_config_map(params['name'], params['domain_id'])

    @transaction
    @check_required(['name', 'domain_id'])
    def get(self, params):
        """Get config map

        Args:
            params (dict): {
                'name': 'str',
                'domain_id': 'str',
                'only': 'list'
            }

        Returns:
            config_map_vo (object)
        """

        return self.config_map_mgr.get_config_map(params['name'], params['domain_id'], params.get('only'))

    @transaction
    @check_required(['domain_id'])
    @append_query_filter(['name', 'domain_id'])
    @append_keyword_filter(['name'])
    def list(self, params):
        """ List config maps

        Args:
            params (dict): {
                'name': 'str',
                'domain_id': 'str',
                'query': 'dict (spaceone.api.core.v1.Query)'
            }

        Returns:
            config_map_vos (objects)
            total_count (int)
        """

        query = params.get('query', {})
        return self.config_map_mgr.list_config_maps(query)

    @transaction
    @check_required(['query', 'domain_id'])
    @append_query_filter(['domain_id'])
    def stat(self, params):
        """
        Args:
            params (dict): {
                'domain_id': 'str',
                'query': 'dict (spaceone.api.core.v1.StatisticsQuery)'
            }

        Returns:
            values (list) : 'list of statistics data'

        """

        query = params.get('query', {})
        return self.config_map_mgr.state_config_maps(query)
