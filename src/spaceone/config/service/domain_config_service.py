import logging

from spaceone.core.service import *
from spaceone.core import utils
from spaceone.config.manager.domain_config_manager import DomainConfigManager

_LOGGER = logging.getLogger(__name__)


@authentication_handler
@authorization_handler
@mutation_handler
@event_handler
class DomainConfigService(BaseService):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.domain_config_mgr: DomainConfigManager = self.locator.get_manager('DomainConfigManager')

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
    @check_required(['name', 'data', 'domain_id'])
    def create(self, params):
        """Create config map

        Args:
            params (dict): {
                'name': 'str',
                'data': 'dict',
                'schema': 'str',
                'tags': 'dict',
                'domain_id': 'str'
            }

        Returns:
            domain_config_vo (object)
        """

        if 'tags' in params:
            params['tags'] = utils.dict_to_tags(params['tags'])

        return self.domain_config_mgr.create_domain_config(params)

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
    @check_required(['name', 'domain_id'])
    def update(self, params):
        """Update config map

        Args:
            params (dict): {
                'name': 'str',
                'data': 'dict',
                'schema': 'str',
                'tags': 'dict',
                'domain_id': 'str'
            }

        Returns:
            domain_config_vo (object)
        """

        if 'tags' in params:
            params['tags'] = utils.dict_to_tags(params['tags'])

        return self.domain_config_mgr.update_domain_config(params)

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
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

        self.domain_config_mgr.delete_domain_config(params['name'], params['domain_id'])

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
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
            domain_config_vo (object)
        """

        return self.domain_config_mgr.get_domain_config(params['name'], params['domain_id'], params.get('only'))

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
    @check_required(['domain_id'])
    @append_query_filter(['name', 'domain_id'])
    @change_tag_filter('tags')
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
            domain_config_vos (objects)
            total_count (int)
        """

        query = params.get('query', {})
        return self.domain_config_mgr.list_domain_configs(query)

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
    @check_required(['query', 'domain_id'])
    @append_query_filter(['domain_id'])
    @change_tag_filter('tags')
    @append_keyword_filter(['name'])
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
        return self.domain_config_mgr.state_domain_configs(query)
