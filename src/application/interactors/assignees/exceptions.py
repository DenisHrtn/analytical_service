from base_exception import BaseAppException


class AssigneeAlreadyExistsException(BaseAppException):
    def __init__(self):
        super().__init__('Assignee Already Exists', 400)
