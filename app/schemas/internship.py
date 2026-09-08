from datetime import date
from pydantic import BaseModel


class InternshipOut(BaseModel):
    id: int
    student_id: int
    company_name: str
    internship_type: str | None
    start_date: date | None
    end_date: date | None
    duration_days: int | None
    domain: str | None
    role: str | None
    stipend: float | None
    location: str | None
    completion_status: str
    certificate_available: bool

    model_config = {"from_attributes": True}
