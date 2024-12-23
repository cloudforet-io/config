from spaceone.core.pygrpc.server import GRPCServer
from spaceone.config.interface.grpc.user_config import UserConfig
from spaceone.config.interface.grpc.domain_config import DomainConfig
from spaceone.config.interface.grpc.shared_config import SharedConfig
from spaceone.config.interface.grpc.public_config import PublicConfig

_all_ = ["app"]

app = GRPCServer()
app.add_service(UserConfig)
app.add_service(DomainConfig)
app.add_service(SharedConfig)
app.add_service(PublicConfig)
