from datetime import datetime

from src.app.auth.models import BlacklistedToken


async def flushexpiredtokens() -> None:
    await BlacklistedToken.objects.filter(
        expires_at__lt=datetime.utcnow()
    ).delete(each=True)
    print('Expired tokens flushed successfully')
