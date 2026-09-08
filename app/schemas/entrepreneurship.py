from pydantic import BaseModel


class EntrepreneurshipOut(BaseModel):
    id: int
    student_id: int
    startup_name: str
    startup_type: str | None
    industry: str | None
    founding_year: int | None
    role: str | None
    funding_stage: str | None
    funding_amount: float | None
    employees: int | None
    status: str

    model_config = {"from_attributes": True}
