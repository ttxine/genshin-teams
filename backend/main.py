from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

from src.core.db import database
from src.app.auth.routes import auth_router
from src.app.user.routes import user_router
from src.config import settings


app = FastAPI(
    docs_url='{}docs'.format(settings.API_PREFIX),
    redoc_url='{}redoc'.format(settings.API_PREFIX)
)

app.mount('/media', StaticFiles(directory='media'), name='media')

app.state.database = database


@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()


app.include_router(auth_router, prefix='{}auth'.format(settings.API_PREFIX))
app.include_router(user_router, prefix='{}users'.format(settings.API_PREFIX))


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
