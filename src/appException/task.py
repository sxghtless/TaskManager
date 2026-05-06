from utils.app_exception import AppExceptionCase


class TaskNotFound(AppExceptionCase):
    message = "task not found"
    status_code = 404

    def __init__(self) -> None:
        super().__init__(self.status_code, self.message)

class TaskStatusRollbackForbidden(AppExceptionCase):
    message = "Jumping back from 'DONE' is not possible"
    status_code = 400

    def __init__(self) -> None:
        super().__init__(self.status_code, self.message)