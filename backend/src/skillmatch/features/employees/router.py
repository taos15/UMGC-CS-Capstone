from fastapi import APIRouter, HTTPException

from skillmatch.features.auth.dependencies import ADMIN_ROLES, READ_ROLES, role_access

from skillmatch.features.employees.repository import get_employee, get_employees
from skillmatch.features.employees.schemas import Employee


router = APIRouter()


@router.get("/api/v1/employees", response_model=list[Employee],
         **role_access(*READ_ROLES),
         description="Allowed roles: ADMIN, SUPERVISOR, VIEWER.")
def list_employees() -> list[Employee]:
    return get_employees()


@router.get("/api/v1/employees/{employee_id}", response_model=Employee,
         **role_access(*READ_ROLES),
         description="Allowed roles: ADMIN, SUPERVISOR, VIEWER.")
def retrieve_employee(employee_id: str) -> Employee:
    employee = get_employee(employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

UNIMPLEMENTED = {501: {'description': 'Endpoint is not implemented yet.',
    'content': {'application/problem+json': {'schema': {'$ref': '#/components/schemas/ProblemDetails'}}}}}


@router.post('/api/v1/employees', tags=['employees'], responses=UNIMPLEMENTED, status_code=501,
             **role_access(*ADMIN_ROLES), description='Allowed roles: ADMIN.')
def create_employee():
    raise HTTPException(status_code=501, detail='Not implemented')


@router.put('/api/v1/employees/{employee_id}', tags=['employees'], responses=UNIMPLEMENTED, status_code=501,
            **role_access(*ADMIN_ROLES), description='Allowed roles: ADMIN.')
def update_employee(employee_id: str):
    raise HTTPException(status_code=501, detail='Not implemented')
