import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    NAME: str = "governance"
    NETWORK_NAME: str = "mainnet"

    # Ports
    PORT: int = 8000
    HEALTH_PORT: int = 8180
    METRICS_PORT: int = 9400

    METRICS_ADDRESS: str = "localhost"

    # Prefix
    REST_PREFIX: str = "/api/v1"
    HEALTH_PREFIX: str = "/heath"
    METRICS_PREFIX: str = "/metrics"
    DOCS_PREFIX: str = "/api/v1/docs"

    CORS_ALLOW_ORIGINS: str = "*"
    CORS_ALLOW_CREDENTIALS: bool = False
    CORS_ALLOW_METHODS: str = "GET,POST,HEAD,OPTIONS"
    CORS_ALLOW_HEADERS: str = ""
    CORS_EXPOSE_HEADERS: str = "x-total-count"

    # Monitoring
    HEALTH_POLLING_INTERVAL: int = 60

    # ICON Nodes
    ICON_NODE_URL: str = "https://api.icon.community/api/v3"
    # TODO: Remove?
    BACKUP_ICON_NODE_URL: str = "https://ctz.solidwallet.io/api/v3"

    # Community API
    # TODO: Update this when vultr migration is complete
    # COMMUNITY_API_ENDPOINT: str = "https://tracker.icon.community"
    COMMUNITY_API_ENDPOINT: str = "https://tracker.v2.mainnet.sng.vultr.icon.community"


    # DB
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "changeme"
    POSTGRES_SERVER: str = "127.0.0.1"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DATABASE: str = "postgres"

    # Endpoints
    MAX_PAGE_SIZE: int = 100

    CRON_SLEEP_SEC: int = 600

    LOANS_CHART_MIN_TIME_STEP_MIN: int = 60 * 24

    class Config:
        case_sensitive = True


if os.environ.get("ENV_FILE", False):
    settings = Settings(_env_file=os.environ.get("ENV_FILE"))
else:
    # settings = Settings()
    settings = Settings(_env_file=os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', '.env.mainnet'))
