from datetime import datetime
from pydantic import BaseModel


class InstitutionOut(BaseModel):
    id: int
    institution_code: str
    name: str
    type: str
    city: str
    state: str
    country: str
    established_year: int
    accreditation: str | None
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
