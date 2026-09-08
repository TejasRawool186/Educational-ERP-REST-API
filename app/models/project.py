from datetime import date
from sqlalchemy import Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    project_title: Mapped[str] = mapped_column(String(300), nullable=False)
    project_type: Mapped[str | None] = mapped_column(String(50))   # major, minor, research
    domain: Mapped[str | None] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text)
    start_date: Mapped[date | None] = mapped_column(Date)
    end_date: Mapped[date | None] = mapped_column(Date)
    technology_stack: Mapped[str | None] = mapped_column(String(500))
    guide_faculty_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("faculty.id"), nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="completed")

    student: Mapped["Student"] = relationship("Student", back_populates="projects")
    guide_faculty: Mapped["Faculty | None"] = relationship("Faculty")
