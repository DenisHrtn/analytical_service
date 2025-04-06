from base_exception import BaseAppException


class TaskAlreadyExists(BaseAppException):
    def __init__(self):
        super().__init__("Task already exists.", 400)
