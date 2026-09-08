from datetime import date
from pydantic import BaseModel


class ProfessionalActivityOut(BaseModel):
    id: int
    student_id: int
    activity_type: str
    title: str
    organization: str | None
    activity_date: date | None
    role: str | None
    outcome: str | None
    certificate_available: bool

    model_config = {"from_attributes": True}
