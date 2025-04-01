from application.interactors.base_exception import BaseInteractorException


class AssigneeAlreadyExistsException(BaseInteractorException):
    def __init__(self):
        super().__init__('Assignee Already Exists', 400)
