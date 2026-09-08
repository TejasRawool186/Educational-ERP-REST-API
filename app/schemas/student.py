from datetime import date, datetime
from pydantic import BaseModel


class StudentOut(BaseModel):
    id: int
    student_uid: str
    institution_id: int
    campus_id: int
    department_id: int
    program_id: int
    roll_number: str
    first_name: str
    middle_name: str | None
    last_name: str
    full_name: str
    gender: str | None
    date_of_birth: date | None
    category: str | None
    admission_type: str | None
    admission_year: int
    batch_year: int
    graduation_year: int | None
    current_semester: int | None
    current_status: str
    email: str | None
    phone: str | None
    city: str | None
    state: str | None
    country: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class StudentSummary(BaseModel):
    """Lightweight projection for list endpoints."""
    student_uid: str
    full_name: str
    department_id: int
    program_id: int
    batch_year: int
    current_status: str

    model_config = {"from_attributes": True}
