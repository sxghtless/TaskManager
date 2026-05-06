from utils.app_exception import AppExceptionCase


class TaskNotFound(AppExceptionCase):
    message = "task not found"
    status_code = 404

    def __init__(self) -> None:
        super().__init__(self.status_code, self.message)

class TaskStatusRollbackForbidden(AppExceptionCase):
    status_code = 400

    def __init__(self, from_status: str, to_status: str) -> None:
        super().__init__(self.status_code,f"cannot transition from '{from_status}' to '{to_status}'"
        )