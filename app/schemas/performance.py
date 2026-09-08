from datetime import datetime
from pydantic import BaseModel


class PerformanceOut(BaseModel):
    id: int
    student_id: int
    semester: int
    academic_year: str
    sgpa: float | None
    cgpa: float | None
    credits_registered: int | None
    credits_earned: int | None
    backlogs_count: int
    result_status: str
    class_rank: int | None
    department_rank: int | None
    created_at: datetime

    model_config = {"from_attributes": True}
