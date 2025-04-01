from application.interactors.base_exception import BaseInteractorException


class TaskAlreadyExists(BaseInteractorException):
    def __init__(self):
        super().__init__("Task already exists.", 400)
