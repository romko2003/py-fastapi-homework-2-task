from contextlib import asynccontextmanager

from fastapi import FastAPI

# ці імена мають експортуватися з database/__init__.py
from database import init_db, close_db
# а цей — з routes/__init__.py
from routes import movie_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    # створюємо таблиці/конекшн при старті
    await init_db()
    try:
        yield
    finally:
        # акуратно закриваємо ресурси при зупинці
        await close_db()


app = FastAPI(
    title="Movies homework",
    description="Description of project",
    lifespan=lifespan,
)

api_version_prefix = "/api/v1"

# /api/v1/theater/movies/...
app.include_router(
    movie_router,
    prefix=f"{api_version_prefix}/theater",
    tags=["theater"],
)
