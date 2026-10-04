"""Problem responses and per-request correlation for authentication."""

import logging
import re
from http import HTTPStatus
from uuid import uuid4

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field
from starlette.datastructures import Headers, MutableHeaders
from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Message, Receive, Scope, Send


class FieldError(BaseModel):
    field: str
    code: str
    message: str


class ProblemDetails(BaseModel):
    type: str = 'about:blank'
    title: str
    status: int
    code: str
    request_id: str
    detail: str
    field_errors: list[FieldError] = Field(default_factory=list)


class ProblemError(Exception):
    def __init__(self, status: int, code: str, detail: str):
        self.status = status
        self.code = code
        self.detail = detail


def problem_response(status: int, code: str, detail: str, request_id: str,
                     field_errors: list[FieldError] | None = None) -> JSONResponse:
    body = ProblemDetails(title=HTTPStatus(status).phrase, status=status, code=code,
                          detail=detail, request_id=request_id, field_errors=field_errors or [])
    headers = {'X-Request-ID': request_id, 'Cache-Control': 'no-store'}
    if status == 401:
        headers['WWW-Authenticate'] = 'Bearer'
    return JSONResponse(body.model_dump(), status_code=status,
                        media_type='application/problem+json', headers=headers)


async def problem_handler(request: Request, exc: ProblemError) -> JSONResponse:
    return problem_response(exc.status, exc.code, exc.detail, request.state.request_id)


async def validation_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    # Do not serialize input/body/context: they can contain credentials.
    fields = [FieldError(field='.'.join(map(str, error['loc'])),
                         code=error['type'], message=error['msg']) for error in exc.errors()]
    return problem_response(422, 'VALIDATION_ERROR', 'Request validation failed.',
                            request.state.request_id, fields)


class RequestIDMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope['type'] != 'http':
            await self.app(scope, receive, send)
            return
        incoming = Headers(scope=scope).get('x-request-id', '')
        request_id = incoming if re.fullmatch(r'[A-Za-z0-9._-]{1,128}', incoming) else str(uuid4())
        scope.setdefault('state', {})['request_id'] = request_id
        started = False

        async def correlated_send(message: Message) -> None:
            nonlocal started
            if message['type'] == 'http.response.start':
                MutableHeaders(scope=message)['X-Request-ID'] = request_id
                started = True
            await send(message)

        try:
            await self.app(scope, receive, correlated_send)
        except Exception:
            logging.getLogger(__name__).exception('Unhandled error request_id=%s', request_id)
            if started:
                raise
            await problem_response(500, 'INTERNAL_ERROR', 'An unexpected error occurred.',
                                   request_id)(scope, receive, correlated_send)
