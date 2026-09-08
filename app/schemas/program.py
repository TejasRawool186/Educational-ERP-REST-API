from pydantic import BaseModel


class ProgramOut(BaseModel):
    id: int
    department_id: int
    program_code: str
    name: str
    degree_type: str
    duration_years: int
    total_semesters: int
    intake_capacity: int | None
    accreditation_status: str | None
    status: str

    model_config = {"from_attributes": True}
