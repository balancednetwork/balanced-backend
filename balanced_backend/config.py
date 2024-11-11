from __future__ import annotations

import os

from dotenv import dotenv_values

from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    NAME: str = "balanced-backend"
    NETWORK_NAME: str = "mainnet"  # Not used?
    VERSION: str = "v0.8.2"  # x-release-please-version

    CHAIN_ID: int = 1  # 1 mainnet, 2 sejong, 7 lisbon

    # Debug
    VERBOSE: bool = False

    # Ports
    PORT: int = 8000
    METRICS_PORT: int = 9400
    METRICS_ADDRESS: str = "localhost"

    # Prefix
    REST_PREFIX: str = "/api/v1"
    HEALTH_PREFIX: str = "/health"
    READINESS_PREFIX: str = "/ready"
    METRICS_PREFIX: str = "/metrics"
    DOCS_PREFIX: str = "/api/v1/docs"
    # HEALTH_POLLING_INTERVAL: int = 60

    CORS_ALLOW_ORIGINS: str = "*"
    CORS_ALLOW_CREDENTIALS: bool = False
    CORS_ALLOW_METHODS: str = "GET,POST,HEAD,OPTIONS"
    CORS_ALLOW_HEADERS: str = ""
    CORS_EXPOSE_HEADERS: str = "x-total-count"

    # ICON Nodes
    ICON_NODE_URL: str = "https://api.icon.community/api/v3"
    BACKUP_ICON_NODE_URL: str = "https://ctz.solidwallet.io/api/v3"

    # Community API
    COMMUNITY_API_ENDPOINT: str = "https://tracker.icon.community"

    # # DB
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "changeme"
    POSTGRES_SERVER: str = "127.0.0.1"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DATABASE: str = "postgres"

    # Kafka
    KAFKA_BROKER_URL: str = "localhost:29092"
    CONSUMER_GROUP: str = "balanced2"
    CONSUMER_AUTO_OFFSET_RESET: str = "earliest"
    CONSUMER_TOPIC_BLOCKS: str = "blocks"
    CONSUMER_END_BLOCK: int | None = None

    # Endpoints
    MAX_PAGE_SIZE: int = 100

    LOANS_CHART_MIN_TIME_STEP_MIN: int = 60 * 24

    FIRST_BLOCK: int = 33518615
    FIRST_BLOCK_TIMESTAMP: int | None = None  # Will be updated in volumes cron
    BLOCK_SYNC_CHUNK: int = 10000  # For 20M blocks this is 2000 gets
    MAX_TS_RECORDS: int = 5000

    COINGECKO_LIQUIDITY_CUTOFF: int = 1000
    COINGECKO_DISABLE: bool = False
    COINGECKO_HACK: bool = False

    # class Config:
    #     case_sensitive = True

    model_config = SettingsConfigDict(
        case_sensitive=True,
    )



def load_env_to_variables(env_file_path):
    """
    Load environment variables from a .env file and export them to the actual environment variables.

    Args:
    - env_file_path (str): Path to the .env file

    Returns:
    - None
    """
    # Load environment variables from the .env file
    env_vars = dotenv_values(env_file_path)

    # Export variables to the actual environment
    for key, value in env_vars.items():
        os.environ[key] = value


# Ignored by default
test_env = os.path.join(os.path.dirname(__file__), "..", ".env.test")
if os.environ.get("ENV_FILE", False):
    load_env_to_variables(os.environ.get("ENV_FILE"))
elif os.path.isfile(test_env):
    load_env_to_variables(test_env)

settings = Settings()
