from datetime import date
from pydantic import BaseModel


class AwardOut(BaseModel):
    id: int
    student_id: int
    faculty_id: int | None
    award_name: str
    award_category: str | None
    awarding_body: str | None
    award_date: date | None
    level: str | None
    position: str | None
    description: str | None

    model_config = {"from_attributes": True}
