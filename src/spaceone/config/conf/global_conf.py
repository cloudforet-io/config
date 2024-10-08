# Database Settings
DATABASE_AUTO_CREATE_INDEX = True
DATABASES = {
    "default": {
        "db": "config",
        "host": "localhost",
        "port": 27017,
        "username": "",
        "password": "",
    }
}

# Cache Settings
CACHES = {
    "default": {},
    "local": {
        "backend": "spaceone.core.cache.local_cache.LocalCache",
        "max_size": 128,
        "ttl": 300,
    },
}

# Handler Settings
HANDLERS = {
    # "authentication": [{
    #     "backend": "spaceone.core.handler.authentication_handler:SpaceONEAuthenticationHandler"
    # }],
    # "authorization": [{
    #     "backend": "spaceone.core.handler.authorization_handler:SpaceONEAuthorizationHandler"
    # }],
    # "mutation": [{
    #     "backend": "spaceone.core.handler.mutation_handler:SpaceONEMutationHandler"
    # }],
    # "event": []
}

# Connector Settings
CONNECTORS = {}

# System Token Settings
TOKEN = ""

# Default Domain Unified Cost Configuration
DEFAULT_UNIFIED_COST_CONFIG = {

    "run_hour": 0,
    "aggregation_day": 15,
    "is_last_day": False,
    "exchange_source": "Yahoo Finance!",
    "exchange_date": 15,
    "is_exchange_last_day": False,
    "exchange_rate_mode": "AUTO",
    # "custom_exchange_rate": {},
    "currency": "KRW",
}
