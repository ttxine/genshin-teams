import asyncio
import sys
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from scripts import createsuperuser, startserver, flushexpiredtokens, loadgenshindata
from scripts.exceptions import CommandException
from src.core.db import database
from src.app.auth.routes import auth_router
from src.app.user.routes import user_router
from src.app.planner.routers import weapon_main_router, artifact_router
from src.config import settings


app = FastAPI(
    docs_url='{}/docs'.format(settings.API_DEVELOP_PREFIX),
    redoc_url='{}/redoc'.format(settings.API_DEVELOP_PREFIX),
    swagger_ui_parameters={
        'docExpansion': 'none'
    }
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


app.include_router(auth_router, prefix='{}/auth'.format(settings.API_DEVELOP_PREFIX))
app.include_router(user_router, prefix='{}/users'.format(settings.API_DEVELOP_PREFIX))
app.include_router(weapon_main_router, prefix='{}/weapons'.format(settings.API_DEVELOP_PREFIX))
app.include_router(artifact_router, prefix='{}'.format(settings.API_DEVELOP_PREFIX))


if __name__ == '__main__':
    args = []
    try:
        command = sys.argv
        script = command[1]
        if len(command) > 2:
            args.append(sys.argv[2])
        function = globals()[script]
    except IndexError:
        raise CommandException('No command given')
    except KeyboardInterrupt:
        print('\n\nCommand execution interrupted')
        sys.exit(0)
    if asyncio.iscoroutinefunction(function):
        asyncio.run(function(*args))
    else:
        function(*args)
