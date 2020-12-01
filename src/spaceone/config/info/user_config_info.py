import functools
from spaceone.api.core.v1 import tag_pb2
from spaceone.api.config.v1 import user_config_pb2
from spaceone.core.pygrpc.message_type import *
from spaceone.config.model.user_config_model import UserConfig

__all__ = ['UserConfigInfo', 'UserConfigsInfo']


def UserConfigInfo(user_config_vo: UserConfig, minimal=False):
    info = {
        'name': user_config_vo.name,
    }

    if not minimal:
        info.update({
            'data': change_struct_type(user_config_vo.data),
            'tags': [tag_pb2.Tag(key=tag.key, value=tag.value) for tag in user_config_vo.tags],
            'domain_id': user_config_vo.domain_id,
            'created_at': change_timestamp_type(user_config_vo.created_at)
        })

    return user_config_pb2.UserConfigInfo(**info)


def UserConfigsInfo(user_config_vos, total_count, **kwargs):
    return user_config_pb2.UserConfigsInfo(results=list(
        map(functools.partial(UserConfigInfo, **kwargs), user_config_vos)), total_count=total_count)
