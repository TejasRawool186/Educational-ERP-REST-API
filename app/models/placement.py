from datetime import date
from sqlalchemy import Date, ForeignKey, Index, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Placement(Base):
    __tablename__ = "placements"
    __table_args__ = (
        Index("ix_placements_student", "student_id"),
        Index("ix_placements_company", "company_name"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    company_name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    company_type: Mapped[str | None] = mapped_column(String(50))
    industry: Mapped[str | None] = mapped_column(String(100))
    placement_type: Mapped[str | None] = mapped_column(String(50))
    job_role: Mapped[str | None] = mapped_column(String(100))
    package_lpa: Mapped[float | None] = mapped_column(Numeric(8, 2))
    base_salary: Mapped[float | None] = mapped_column(Numeric(10, 2))
    bonus: Mapped[float | None] = mapped_column(Numeric(10, 2))
    placement_date: Mapped[date | None] = mapped_column(Date)
    offer_date: Mapped[date | None] = mapped_column(Date)
    location: Mapped[str | None] = mapped_column(String(100))
    offer_status: Mapped[str] = mapped_column(String(30), nullable=False, default="accepted")
    joining_status: Mapped[str | None] = mapped_column(String(30))

    student: Mapped["Student"] = relationship("Student", back_populates="placements")
