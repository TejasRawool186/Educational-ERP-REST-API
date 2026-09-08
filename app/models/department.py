from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Department(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    campus_id: Mapped[int] = mapped_column(Integer, ForeignKey("campuses.id"), nullable=False, index=True)
    department_code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    short_name: Mapped[str | None] = mapped_column(String(20))
    hod_faculty_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("faculty.id"), nullable=True)
    established_year: Mapped[int | None] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="active")

    campus: Mapped["Campus"] = relationship("Campus", back_populates="departments")
    programs: Mapped[list["Program"]] = relationship("Program", back_populates="department")
    faculty: Mapped[list["Faculty"]] = relationship(
        "Faculty", back_populates="department", foreign_keys="[Faculty.department_id]"
    )
    students: Mapped[list["Student"]] = relationship("Student", back_populates="department")
    courses: Mapped[list["Course"]] = relationship("Course", back_populates="department")
