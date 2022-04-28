from src.app.base.services import ModelService
from src.app.planner.models import teams as models


class TeamService(ModelService):
    model = models.Team
