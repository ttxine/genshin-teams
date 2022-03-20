import uvicorn

from scripts.exceptions import CommandException

ACTIONS = {
    '--reload': '_set_reload_true'
}


def _set_reload_true() -> dict:
    return {'reload': True}


def startserver(option: str | None = None) -> None:
    kw = {}
    if option:
        try:
            action = ACTIONS[option]
            kw = globals()[action]()
        except KeyError:
            raise CommandException('Invalid argument')
    uvicorn.run('main:app', **kw)
