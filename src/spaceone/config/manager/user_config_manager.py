import logging

from spaceone.core.manager import BaseManager
from spaceone.config.model.user_config_model import UserConfig

_LOGGER = logging.getLogger(__name__)


class UserConfigManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_config_model: UserConfig = self.locator.get_model('UserConfig')

    def create_user_config(self, params):
        def _rollback(user_config_vo):
            _LOGGER.info(f'[create_user_config._rollback] '
                         f'Delete config map : {user_config_vo.name}')
            user_config_vo.delete()

        user_config_vo: UserConfig = self.user_config_model.create(params)
        self.transaction.add_rollback(_rollback, user_config_vo)

        return user_config_vo

    def update_user_config(self, params):
        user_config_vo: UserConfig = self.get_user_config(params['name'], params['domain_id'])
        return self.update_user_config_by_vo(params, user_config_vo)

    def update_user_config_by_vo(self, params, user_config_vo):
        def _rollback(old_data):
            _LOGGER.info(f'[update_user_config_by_vo._rollback] Revert Data : {old_data["name"]}')
            user_config_vo.update(old_data)

        self.transaction.add_rollback(_rollback, user_config_vo.to_dict())

        return user_config_vo.update(params)

    def delete_user_config(self, name, domain_id):
        user_config_vo: UserConfig = self.get_user_config(name, domain_id)
        user_config_vo.delete()

    def get_user_config(self, name, domain_id, only=None):
        return self.user_config_model.get(name=name, domain_id=domain_id, only=only)

    def list_user_configs(self, query={}):
        return self.user_config_model.query(**query)

    def state_user_configs(self, query):
        return self.user_config_model.stat(**query)
