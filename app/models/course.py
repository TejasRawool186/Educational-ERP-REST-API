from sqlalchemy import ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    department_id: Mapped[int] = mapped_column(Integer, ForeignKey("departments.id"), nullable=False, index=True)
    program_id: Mapped[int] = mapped_column(Integer, ForeignKey("programs.id"), nullable=False, index=True)

    course_code: Mapped[str] = mapped_column(String(30), unique=True, nullable=False, index=True)
    course_name: Mapped[str] = mapped_column(String(200), nullable=False)
    course_type: Mapped[str] = mapped_column(String(50), nullable=False, default="theory")

    credits: Mapped[float] = mapped_column(Numeric(4, 1), nullable=False, default=3.0)
    lecture_hours: Mapped[int | None] = mapped_column(Integer)
    tutorial_hours: Mapped[int | None] = mapped_column(Integer)
    practical_hours: Mapped[int | None] = mapped_column(Integer)

    semester: Mapped[int] = mapped_column(Integer, nullable=False)
    academic_year: Mapped[str | None] = mapped_column(String(10))

    faculty_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("faculty.id"), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="active")

    department: Mapped["Department"] = relationship("Department", back_populates="courses")
    program: Mapped["Program"] = relationship("Program", back_populates="courses")
    faculty_member: Mapped["Faculty | None"] = relationship("Faculty", back_populates="courses")
    enrollments: Mapped[list["Enrollment"]] = relationship("Enrollment", back_populates="course")
