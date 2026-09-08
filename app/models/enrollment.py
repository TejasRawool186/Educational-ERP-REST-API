from datetime import date
from sqlalchemy import Date, ForeignKey, Index, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Enrollment(Base):
    __tablename__ = "enrollments"
    __table_args__ = (
        Index("ix_enrollments_student_course", "student_id", "course_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    course_id: Mapped[int] = mapped_column(Integer, ForeignKey("courses.id"), nullable=False, index=True)
    academic_year: Mapped[str] = mapped_column(String(10), nullable=False)
    semester: Mapped[int] = mapped_column(Integer, nullable=False)
    enrollment_date: Mapped[date | None] = mapped_column(Date)
    attendance_requirement: Mapped[float | None] = mapped_column(Numeric(5, 2), default=75.0)
    enrollment_status: Mapped[str] = mapped_column(String(30), nullable=False, default="active")

    student: Mapped["Student"] = relationship("Student", back_populates="enrollments")
    course: Mapped["Course"] = relationship("Course", back_populates="enrollments")
