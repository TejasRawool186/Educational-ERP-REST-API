from datetime import date, datetime
from pydantic import BaseModel


class FacultyOut(BaseModel):
    id: int
    faculty_uid: str
    department_id: int
    employee_code: str
    first_name: str
    last_name: str
    full_name: str
    designation: str | None
    qualification: str | None
    specialization: str | None
    joining_date: date | None
    experience_years: float | None
    email: str | None
    phone: str | None
    employment_type: str
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
