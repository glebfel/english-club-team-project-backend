from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi import status
from pydantic.error_wrappers import ErrorWrapper

from exceptions import DatabaseNotFoundError


def convert_sqlalchemy_row_to_dict(row) -> dict:
    d = {}
    for column in row.__table__.columns:
        d[column.name] = getattr(row, column.name)
    return d


def common_error_handler_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            arg = 'start_date' if 'Start date must be before end date' in str(e) else 'end_date'
            raise RequestValidationError([ErrorWrapper(e, ('body', arg))])
        except DatabaseNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    return wrapper
