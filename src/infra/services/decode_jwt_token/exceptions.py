from base_exception import BaseAppException


class TokenNotFoundException(BaseAppException):
    def __init__(self):
        super().__init__("Token not found", 400)
