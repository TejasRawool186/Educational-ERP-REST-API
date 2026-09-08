from sqlalchemy import ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Grade(Base):
    __tablename__ = "grades"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    course_id: Mapped[int] = mapped_column(Integer, ForeignKey("courses.id"), nullable=False, index=True)
    semester: Mapped[int] = mapped_column(Integer, nullable=False)
    academic_year: Mapped[str] = mapped_column(String(10), nullable=False)
    grade: Mapped[str | None] = mapped_column(String(5))
    grade_point: Mapped[float | None] = mapped_column(Numeric(4, 2))
    credits: Mapped[float | None] = mapped_column(Numeric(4, 1))
    result_status: Mapped[str] = mapped_column(String(20), nullable=False, default="pass")

    student: Mapped["Student"] = relationship("Student", back_populates="grades")
    course: Mapped["Course"] = relationship("Course")
