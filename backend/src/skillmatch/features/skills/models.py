from sqlmodel import SQLModel, Field


class SkillRecord(SQLModel, table=True):
    __tablename__ = 'skills'
    skill_id: str = Field(primary_key=True)
