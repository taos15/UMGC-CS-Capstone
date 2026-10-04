"""Endpoint stubs; role annotations are documentation only."""

from fastapi import APIRouter, HTTPException

router = APIRouter()

UNIMPLEMENTED = {501: {'description': 'Endpoint is not implemented yet.'}}


@router.post('/api/v1/auth/login', tags=['auth'], responses=UNIMPLEMENTED, status_code=501,
             openapi_extra={'x-allowed-roles': [], 'security': []}, description='Public.')
def login():
    raise HTTPException(status_code=501, detail='Not implemented')
