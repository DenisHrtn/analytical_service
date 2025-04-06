from base_exception import BaseAppException


class ProjectAlreadyExists(BaseAppException):
    def __init__(self):
        super().__init__("Project already exists", 400)


class ProjectDoesNotExist(BaseAppException):
    def __init__(self):
        super().__init__("Project does not exist", 404)


class ProjectBaseException(BaseAppException):
    def __init__(self):
        super().__init__("Something wrong...", 500)
