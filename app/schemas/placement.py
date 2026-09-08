from datetime import date
from pydantic import BaseModel


class PlacementOut(BaseModel):
    id: int
    student_id: int
    company_name: str
    company_type: str | None
    industry: str | None
    placement_type: str | None
    job_role: str | None
    package_lpa: float | None
    base_salary: float | None
    bonus: float | None
    placement_date: date | None
    offer_date: date | None
    location: str | None
    offer_status: str
    joining_status: str | None

    model_config = {"from_attributes": True}
