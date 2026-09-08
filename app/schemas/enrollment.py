from datetime import date
from pydantic import BaseModel


class EnrollmentOut(BaseModel):
    id: int
    student_id: int
    course_id: int
    academic_year: str
    semester: int
    enrollment_date: date | None
    attendance_requirement: float | None
    enrollment_status: str

    model_config = {"from_attributes": True}
