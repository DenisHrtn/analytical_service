import logging
import time

import jwt

from application.interfaces.decode_tokens.decode_tokens import IDecodeTokens
from config import ALGORITHM, SECRET_KEY


logger = logging.getLogger(__name__)


class DecodeJwtToken(IDecodeTokens):
    @staticmethod
    async def decode_token(token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            expiration = payload['exp']
            current_time = time.time()

            logger.info(
                f"exp в токене: {expiration}, текущее Unix-время сервера: {current_time}"
            )

            return payload
        except Exception as e:
            logger.error(e)
