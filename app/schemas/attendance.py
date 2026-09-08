from pydantic import BaseModel


class AttendanceOut(BaseModel):
    id: int
    student_id: int
    course_id: int
    academic_year: str
    semester: int
    classes_conducted: int
    classes_attended: int
    attendance_percentage: float
    status: str

    model_config = {"from_attributes": True}
