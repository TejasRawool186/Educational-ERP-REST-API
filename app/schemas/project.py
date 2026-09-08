from datetime import date
from pydantic import BaseModel


class ProjectOut(BaseModel):
    id: int
    student_id: int
    project_title: str
    project_type: str | None
    domain: str | None
    description: str | None
    start_date: date | None
    end_date: date | None
    technology_stack: str | None
    guide_faculty_id: int | None
    status: str

    model_config = {"from_attributes": True}
