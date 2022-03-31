import ormar

from src.app.planner.consts import Stat
from src.core.db import BaseMeta


class StatCore(ormar.Model):
    class Meta(BaseMeta):
        abstract = True

    stat: str = ormar.String(max_length=10, choices=list(Stat))
    start_value: float = ormar.Float(minimum=0)
