import logging

from spaceone.core.manager import BaseManager
from spaceone.config.model.domain_config_model import DomainConfig

_LOGGER = logging.getLogger(__name__)


class DomainConfigManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.domain_config_model: DomainConfig = self.locator.get_model('DomainConfig')

    def create_domain_config(self, params):
        def _rollback(domain_config_vo):
            _LOGGER.info(f'[create_domain_config._rollback] '
                         f'Delete domain config : {domain_config_vo.name}')
            domain_config_vo.delete()

        domain_config_vo: DomainConfig = self.domain_config_model.create(params)
        self.transaction.add_rollback(_rollback, domain_config_vo)

        return domain_config_vo

    def update_domain_config(self, params):
        domain_config_vo: DomainConfig = self.get_domain_config(params['name'], params['domain_id'])
        return self.update_domain_config_by_vo(params, domain_config_vo)

    def update_domain_config_by_vo(self, params, domain_config_vo):
        def _rollback(old_data):
            _LOGGER.info(f'[update_domain_config_by_vo._rollback] Revert Data : {old_data["name"]}')
            domain_config_vo.update(old_data)

        self.transaction.add_rollback(_rollback, domain_config_vo.to_dict())

        return domain_config_vo.update(params)

    def delete_domain_config(self, name, domain_id):
        domain_config_vo: DomainConfig = self.get_domain_config(name, domain_id)
        domain_config_vo.delete()

    def get_domain_config(self, name, domain_id, only=None):
        return self.domain_config_model.get(name=name, domain_id=domain_id, only=only)

    def filter_domain_configs(self, **conditions):
        return self.domain_config_model.filter(**conditions)

    def list_domain_configs(self, query={}):
        return self.domain_config_model.query(**query)

    def state_domain_configs(self, query):
        return self.domain_config_model.stat(**query)
