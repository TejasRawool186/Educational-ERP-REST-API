from datetime import date
from sqlalchemy import Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Examination(Base):
    __tablename__ = "examinations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    course_id: Mapped[int] = mapped_column(Integer, ForeignKey("courses.id"), nullable=False, index=True)
    exam_type: Mapped[str] = mapped_column(String(50), nullable=False)   # internal, mid, end-sem
    exam_date: Mapped[date | None] = mapped_column(Date)
    maximum_marks: Mapped[float] = mapped_column(Numeric(6, 2), nullable=False, default=100.0)
    marks_obtained: Mapped[float] = mapped_column(Numeric(6, 2), nullable=False, default=0.0)
    grade: Mapped[str | None] = mapped_column(String(5))
    grade_point: Mapped[float | None] = mapped_column(Numeric(4, 2))
    result_status: Mapped[str] = mapped_column(String(20), nullable=False, default="pass")

    student: Mapped["Student"] = relationship("Student", back_populates="examinations")
    course: Mapped["Course"] = relationship("Course")
