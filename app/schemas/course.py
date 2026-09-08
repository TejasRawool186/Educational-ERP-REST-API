from pydantic import BaseModel


class CourseOut(BaseModel):
    id: int
    department_id: int
    program_id: int
    course_code: str
    course_name: str
    course_type: str
    credits: float
    lecture_hours: int | None
    tutorial_hours: int | None
    practical_hours: int | None
    semester: int
    academic_year: str | None
    faculty_id: int | None
    status: str

    model_config = {"from_attributes": True}
