from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status, Response
from pydantic import ValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import uvicorn
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from app.middleware.prometheus import prometheus_middleware
from app.database.db import init_db
from app.goods.routers.goods import router as router_goods


app = FastAPI()

app.middleware("http")(prometheus_middleware)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    swagger_ui_parameters={"syntaxHighlight": {"theme": "github"}},
    title="Goods API",
    lifespan=lifespan,
    description="Goods tool backend API.",
)


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )


@app.get("/ping")
async def pong():
    return {"ping": "pong!"}

@app.get("/test")
async def test():
    return {"hello": "world!"}

@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )

app.include_router(router_goods)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
