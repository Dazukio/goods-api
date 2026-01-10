import logging
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status, Response
from pydantic import ValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import uvicorn
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
import os
import asyncio

from app.middleware.prometheus import prometheus_middleware
from app.database.db import init_db
from app.goods.routers.goods import router as router_goods

# Настройка логирования в формате JSON для Loki
logging.basicConfig(
    level=logging.INFO,
    format='{"time": "%(asctime)s", "level": "%(levelname)s", "name": "%(name)s", "message": "%(message)s", "service": "goods-api"}',
    datefmt='%Y-%m-%dT%H:%M:%S%z',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("goods-api")

async def wait_for_db():
    """Ожидание доступности базы данных"""
    import asyncpg
    db_url = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres123@db:5432/goods")
    
    # Парсим URL
    from sqlalchemy.engine import make_url
    url = make_url(db_url)
    
    max_retries = 30
    for i in range(max_retries):
        try:
            logger.info(f"Attempting to connect to database (attempt {i+1}/{max_retries})")
            conn = await asyncpg.connect(
                host=url.host,
                port=url.port or 5432,
                user=url.username,
                password=url.password,
                database=url.database
            )
            await conn.close()
            logger.info("Database connection successful")
            return True
        except Exception as e:
            logger.warning(f"Database connection failed: {e}")
            await asyncio.sleep(2)
    
    logger.error("Failed to connect to database after multiple attempts")
    return False

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Goods API application")
    
    # Ждем доступности базы данных
    if not await wait_for_db():
        raise RuntimeError("Database is not available")
    
    await init_db()
    logger.info("Database initialized successfully")
    yield
    logger.info("Shutting down Goods API application")

app = FastAPI(
    swagger_ui_parameters={"syntaxHighlight": {"theme": "github"}},
    title="Goods API",
    lifespan=lifespan,
    description="Goods tool backend API.",
)

# Добавляем middleware для метрик
app.middleware("http")(prometheus_middleware)

# Middleware для логирования запросов
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    
    try:
        response = await call_next(request)
        logger.info(
            f"Request completed: {request.method} {request.url.path} "
            f"Status: {response.status_code}"
        )
        return response
    except Exception as e:
        logger.error(f"Request failed: {request.method} {request.url.path} - {str(e)}")
        raise

@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    logger.warning(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )

@app.get("/ping")
async def pong():
    logger.info("Health check endpoint called")
    return {"ping": "pong!"}

@app.get("/test")
async def test():
    logger.info("Test endpoint called")
    return {"hello": "world!"}

@app.get("/metrics")
def metrics():
    logger.debug("Metrics endpoint called")
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )

app.include_router(router_goods)

if __name__ == "__main__":
    logger.info("Starting Uvicorn server")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_config=None,
        access_log=True
    )
