
class AppException(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ClientNotFoundException(AppException):
    def __init__(self, client_id: str | None = None, email: str | None = None):
        detail = "Client not found"
        if client_id:
            detail = f"Client with id {client_id} not found"
        elif email:
            detail = f"Client with email {email} not found"
        super().__init__(message=detail, status_code=404)


class DuplicateWebhookEventException(AppException):
    def __init__(self, event_id: str):
        super().__init__(
            message=f"Webhook event {event_id} has already been processed",
            status_code=409,
        )


class ValidationException(AppException):
    def __init__(self, detail: str):
        super().__init__(message=detail, status_code=422)

