import sys
import asyncio

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from scripts import createsuperuser, startserver, loadgenshindata
from scripts.exceptions import CommandException
from src.config import settings
from src.core.db import database
from src.app.auth.routes import auth_router
from src.app.user.routes import user_router
from src.app.planner.routers import planner_router


app = FastAPI(
    docs_url='{}/swagger'.format(settings.API_PREFIX),
    redoc_url='{}/docs'.format(settings.API_PREFIX),
    swagger_ui_parameters={
        'docExpansion': 'none'
    },
    title='Genshin Teams',
    description='A tool providing an editor of weapons, artifacts and characters that allows you plan and share your own teams',
)


origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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


app.include_router(auth_router, prefix='{}'.format(settings.API_PREFIX))
app.include_router(user_router, prefix='{}'.format(settings.API_PREFIX))
app.include_router(planner_router, prefix='{}'.format(settings.API_PREFIX))


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
