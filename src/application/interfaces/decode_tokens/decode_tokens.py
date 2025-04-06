from abc import ABC, abstractmethod


class IDecodeTokens(ABC):
    @staticmethod
    @abstractmethod
    async def decode_token(token: str): pass
