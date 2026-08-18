from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI

from .database import Base, engine
from .routes.leads import router as leads_router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="LeadFlow AI",
    description="API de triagem e qualificação de leads para corretoras de seguros.",
    version="1.0.0",
    lifespan=lifespan,
)
app.include_router(leads_router)


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}
