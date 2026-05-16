from fastapi import FastAPI
from app.api.v1 import users, devices, stats


app = FastAPI(
    title="StatsService",
)


app.include_router(users.router, prefix="/api/v1")
app.include_router(devices.router, prefix="/app/v1")
app.include_router(stats.router, prefix="/api/v1")