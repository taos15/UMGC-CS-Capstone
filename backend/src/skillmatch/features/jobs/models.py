"""Persistent canonical jobs; evidence is stored as validated JSON."""
from sqlalchemy import Column, JSON, CheckConstraint
from sqlmodel import Field, SQLModel


class JobRecord(SQLModel, table=True):
    __tablename__ = 'jobs'
    __table_args__ = (CheckConstraint('version >= 1', name='jobs_positive_version'),)
    id: str = Field(primary_key=True)
    job_code: str = Field(unique=True, index=True)
    version: int = 1
    payload: dict = Field(sa_column=Column(JSON, nullable=False))
