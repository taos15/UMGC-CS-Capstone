from fastapi import APIRouter, HTTPException

from skillmatch.features.employees.repository import get_employee, get_employees
from skillmatch.features.employees.schemas import Employee


router = APIRouter()


@router.get("/api/v1/employees", response_model=list[Employee])
def list_employees() -> list[Employee]:
    return get_employees()


@router.get("/api/v1/employees/{employee_id}", response_model=Employee)
def retrieve_employee(employee_id: str) -> Employee:
    employee = get_employee(employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee
