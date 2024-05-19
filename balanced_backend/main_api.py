from multiprocessing.pool import ThreadPool
import uvicorn
from fastapi import FastAPI
from fastapi_health import health
from prometheus_client import start_http_server
from starlette.middleware.cors import CORSMiddleware
from brotli_asgi import BrotliMiddleware

from balanced_backend.api.health import is_database_online, is_cache_updated
from balanced_backend.api.v1.router import api_router
from balanced_backend.config import settings
from balanced_backend.log import logger
from balanced_backend.cache.cache_cron import cache_cron

description = """
Backend that maintains indexes of all pools, tokens, and associated data such as 
 prices, volumes, and fees for the stats page and coin-market-cap data feeds. 
"""

tags_metadata = [
    {"name": "balanced-backend", "description": description, },
]

app = FastAPI(
    title="Balanced Backend Service",
    description=description,
    version=settings.VERSION,
    openapi_tags=tags_metadata,
    openapi_url=f"{settings.DOCS_PREFIX}/openapi.json",
    docs_url=f"{settings.DOCS_PREFIX}",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.CORS_ALLOW_ORIGINS.split(',')],
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=[method.strip() for method in settings.CORS_ALLOW_METHODS.split(',')],
    allow_headers=[header.strip() for header in settings.CORS_ALLOW_HEADERS.split(',')],
    expose_headers=[header.strip() for header in
                    settings.CORS_EXPOSE_HEADERS.split(',')],
)

app.add_middleware(
    BrotliMiddleware,
    quality=8,
)


@app.on_event("startup")
async def setup():
    logger.info("Starting metrics server.")
    metrics_pool = ThreadPool(1)
    metrics_pool.apply_async(start_http_server,
                             (settings.METRICS_PORT, settings.METRICS_ADDRESS))

    logger.info("Starting cache loop...")
    pool = ThreadPool(1)
    pool.apply_async(cache_cron)


logger.info("Starting application...")
# /health
app.add_api_route(settings.HEALTH_PREFIX, health([
    is_database_online,
]))
# /ready
app.add_api_route(settings.READINESS_PREFIX, health([
    is_cache_updated,
]))
# /api/v1
app.include_router(api_router, prefix=settings.REST_PREFIX)

if __name__ == "__main__":
    uvicorn.run(
        "main_api:app",
        host="0.0.0.0",
        port=settings.PORT,
        log_level="info",
        debug=True,
        workers=1,
    )
