from datetime import date
from pydantic import BaseModel


class PublicationOut(BaseModel):
    id: int
    student_id: int
    faculty_id: int | None
    title: str
    publication_type: str | None
    journal_name: str | None
    conference_name: str | None
    publication_date: date | None
    doi: str | None
    indexed: bool
    indexing_database: str | None
    status: str

    model_config = {"from_attributes": True}
