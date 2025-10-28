from fastapi.exceptions import ResponseValidationError, RequestValidationError
from pydantic import ValidationError
from sqlalchemy.exc import TimeoutError
from fastapi import status, Request, FastAPI
from fastapi.responses import JSONResponse


def register_exception_handler(app: FastAPI):

    @app.exception_handler(ResponseValidationError)
    async def response_validation_exception_handler(request: Request, exc: ResponseValidationError):
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                'detail': 'Server response error'
            }
        )

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'detail': 'Error in request',
                'body': exc.errors()
            }
        )

    @app.exception_handler(TimeoutError)
    async def timeout_exception_handler(request: Request, exc: TimeoutError):
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                'detail': 'Out of server resources'
            }
        )

    @app.exception_handler(ValidationError)
    async def validation_error_handler(request: Request, exc: ValidationError):
        errors = []
        for err in exc.errors():
            errors.append({
                "field": err["loc"][-1],
                "message": err["msg"]
            })
        return JSONResponse(
            status_code=422,
            content={"detail": errors}
        )