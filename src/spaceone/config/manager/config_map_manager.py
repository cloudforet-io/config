import logging

from spaceone.core.manager import BaseManager
from spaceone.config.model.config_map_model import ConfigMap

_LOGGER = logging.getLogger(__name__)


class ConfigMapManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_map_model: ConfigMap = self.locator.get_model('ConfigMap')

    def create_config_map(self, params):
        def _rollback(config_map_vo):
            _LOGGER.info(f'[create_config_map._rollback] '
                         f'Delete config map : {config_map_vo.name}')
            config_map_vo.delete()

        config_map_vo: ConfigMap = self.config_map_model.create(params)
        self.transaction.add_rollback(_rollback, config_map_vo)

        return config_map_vo

    def update_config_map(self, params):
        config_map_vo: ConfigMap = self.get_config_map(params['name'], params['domain_id'])
        return self.update_config_map_by_vo(params, config_map_vo)

    def update_config_map_by_vo(self, params, config_map_vo):
        def _rollback(old_data):
            _LOGGER.info(f'[update_config_map_by_vo._rollback] Revert Data : {old_data["name"]}')
            config_map_vo.update(old_data)

        self.transaction.add_rollback(_rollback, config_map_vo.to_dict())

        return config_map_vo.update(params)

    def delete_config_map(self, name, domain_id):
        config_map_vo: ConfigMap = self.get_config_map(name, domain_id)
        config_map_vo.delete()

    def get_config_map(self, name, domain_id, only=None):
        return self.config_map_model.get(name=name, domain_id=domain_id, only=only)

    def list_config_maps(self, query={}):
        return self.config_map_model.query(**query)

    def state_config_maps(self, query):
        return self.config_map_model.stat(**query)
