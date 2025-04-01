from application.interactors.base_exception import BaseInteractorException


class ProjectAlreadyExists(BaseInteractorException):
    def __init__(self):
        super().__init__("Project already exists", 400)


class ProjectDoesNotExist(BaseInteractorException):
    def __init__(self):
        super().__init__("Project does not exist", 404)


class ProjectBaseException(BaseInteractorException):
    def __init__(self):
        super().__init__("Something wrong...", 500)
