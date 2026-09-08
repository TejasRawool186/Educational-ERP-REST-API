from datetime import date
from sqlalchemy import Boolean, Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Publication(Base):
    __tablename__ = "publications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    faculty_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("faculty.id"), nullable=True, index=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    publication_type: Mapped[str | None] = mapped_column(String(50))  # journal, conference, book_chapter
    journal_name: Mapped[str | None] = mapped_column(String(300))
    conference_name: Mapped[str | None] = mapped_column(String(300))
    publication_date: Mapped[date | None] = mapped_column(Date)
    doi: Mapped[str | None] = mapped_column(String(200))
    indexed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    indexing_database: Mapped[str | None] = mapped_column(String(100))  # Scopus, SCI, IEEE …
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="published")

    student: Mapped["Student"] = relationship("Student", back_populates="publications")
    faculty: Mapped["Faculty | None"] = relationship("Faculty")
