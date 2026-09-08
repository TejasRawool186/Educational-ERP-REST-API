from pydantic import BaseModel


class DepartmentOut(BaseModel):
    id: int
    campus_id: int
    department_code: str
    name: str
    short_name: str | None
    hod_faculty_id: int | None
    established_year: int | None
    status: str

    model_config = {"from_attributes": True}
