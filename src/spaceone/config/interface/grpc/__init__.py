from spaceone.core.pygrpc.server import GRPCServer
from spaceone.config.interface.grpc.domain_config import DomainConfig
from spaceone.config.interface.grpc.user_config import UserConfig

_all_ = ["app"]

app = GRPCServer()
app.add_service(DomainConfig)
app.add_service(UserConfig)
