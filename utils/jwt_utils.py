from datetime import datetime, timezone

import jwt
from django.conf import settings


def create_token(user):
    payload = {
        "user_id": user.id,
        "exp": datetime.now(timezone.utc) + settings.TOKEN_EXPIRATION,
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


def decode_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
