from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Program(Base):
    __tablename__ = "programs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    department_id: Mapped[int] = mapped_column(Integer, ForeignKey("departments.id"), nullable=False, index=True)
    program_code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    degree_type: Mapped[str] = mapped_column(String(50), nullable=False)   # B.Tech, M.Tech, MBA …
    duration_years: Mapped[int] = mapped_column(Integer, nullable=False, default=4)
    total_semesters: Mapped[int] = mapped_column(Integer, nullable=False, default=8)
    intake_capacity: Mapped[int | None] = mapped_column(Integer)
    accreditation_status: Mapped[str | None] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="active")

    department: Mapped["Department"] = relationship("Department", back_populates="programs")
    courses: Mapped[list["Course"]] = relationship("Course", back_populates="program")
    students: Mapped[list["Student"]] = relationship("Student", back_populates="program")
