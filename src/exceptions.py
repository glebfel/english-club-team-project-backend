class BaseAPIException(Exception):
    """Base class for all parser errors"""

    def __str__(self):
        return "Something goes wrong with API-service"


class DatabaseElementNotFoundError(BaseAPIException):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return self.msg