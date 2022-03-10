from datetime import datetime
import ormar
from sqlalchemy import func

from src.core.db import BaseMeta
from src.app.user.models import User


class BlacklistedToken(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = 'blacklisted_tokens'

    id: int = ormar.Integer(primary_key=True)
    user: User = ormar.ForeignKey(User, nullable=False)
    token: str = ormar.Text(nullable=False)
    jti: str = ormar.String(max_length=255, nullable=False, unique=True)
    expires_at: datetime = ormar.DateTime(nullable=False)
    blacklisted_at: datetime = ormar.DateTime(server_default=func.now())
