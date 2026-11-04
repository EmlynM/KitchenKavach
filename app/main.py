from typing import Annotated
from fastapi import Depends, FastAPI
from app.config import Settings, get_settings
from app.usage import router as usage_router

app = FastAPI(title="KitchenKavach", version="0.1.0")

SettingsDep = Annotated[Settings, Depends(get_settings)]

app.include_router(usage_router)


@app.get("/health")
def health(settings: SettingsDep) -> dict:
    return {
        "status": "ok",
        "app": settings.app_name,
        "environment": settings.environment
    }