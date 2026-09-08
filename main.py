from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router
from app.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="AI Business Analytics Assistant",
    version="1.0.0",
    description="Natural-language business analytics over trusted SQL/Python metrics.",
    lifespan=lifespan,
)

app.include_router(router)
