from datetime import date
from pydantic import BaseModel


class CertificationOut(BaseModel):
    id: int
    student_id: int
    certification_name: str
    issuing_organization: str | None
    issue_date: date | None
    expiry_date: date | None
    credential_id: str | None
    domain: str | None
    status: str

    model_config = {"from_attributes": True}
