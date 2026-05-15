from fastapi import FastAPI
from app.api.v1 import users, devices


app = FastAPI(
    title="StatsService",
)


app.include_router(users.router, prefix="/api/v1")
app.include_router(devices.router, prefix="/app/v1")