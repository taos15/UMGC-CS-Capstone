from app.data import EMPLOYEES
from app.schemas import Employee


def get_employee(employee_id: str) -> Employee | None:
    return next((employee for employee in EMPLOYEES if employee.id == employee_id), None)


def get_employees(employee_ids: list[str] | None = None) -> list[Employee]:
    if employee_ids is None:
        return EMPLOYEES
    requested_ids = set(employee_ids)
    return [employee for employee in EMPLOYEES if employee.id in requested_ids]
