from pydantic import BaseModel


class HigherStudiesOut(BaseModel):
    id: int
    student_id: int
    institution_name: str
    country: str | None
    program: str | None
    degree_type: str | None
    specialization: str | None
    admission_year: int | None
    graduation_year: int | None
    scholarship: str | None
    status: str

    model_config = {"from_attributes": True}
