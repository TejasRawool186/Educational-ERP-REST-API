from pydantic import BaseModel


class CampusOut(BaseModel):
    id: int
    institution_id: int
    campus_code: str
    name: str
    city: str
    state: str
    address: str | None
    capacity: int | None
    status: str

    model_config = {"from_attributes": True}
