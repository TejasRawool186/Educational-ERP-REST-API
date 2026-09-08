from sqlalchemy import ForeignKey, Index, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Attendance(Base):
    __tablename__ = "attendance"
    __table_args__ = (
        Index("ix_attendance_student_course", "student_id", "course_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    course_id: Mapped[int] = mapped_column(Integer, ForeignKey("courses.id"), nullable=False, index=True)
    academic_year: Mapped[str] = mapped_column(String(10), nullable=False)
    semester: Mapped[int] = mapped_column(Integer, nullable=False)
    classes_conducted: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    classes_attended: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    attendance_percentage: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False, default=0.0)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="active")

    student: Mapped["Student"] = relationship("Student", back_populates="attendances")
    course: Mapped["Course"] = relationship("Course")
