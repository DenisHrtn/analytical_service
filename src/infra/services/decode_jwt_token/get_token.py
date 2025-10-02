from .exceptions import TokenNotFoundException

from .decode_jwt_token import DecodeJwtToken

from fastapi import Request


async def get_token(request: Request):
    token = request.headers.get('Authorization')

    if not token or not token.startswith('Bearer '):
        raise TokenNotFoundException()

    extracted_token = token.split(' ')[1]

    payload = await DecodeJwtToken.decode_token(token=extracted_token)

    user_id = payload['user_id']

    return user_id
