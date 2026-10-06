"""Persistent canonical employees; evidence is stored as validated JSON."""
from sqlalchemy import Column, JSON, CheckConstraint
from sqlmodel import Field, SQLModel


class EmployeeRecord(SQLModel, table=True):
    __tablename__ = 'employees'
    __table_args__ = (CheckConstraint('version >= 1', name='employees_positive_version'),)
    id: str = Field(primary_key=True)
    employee_number: str = Field(unique=True, index=True)
    version: int = 1
    payload: dict = Field(sa_column=Column(JSON, nullable=False))
