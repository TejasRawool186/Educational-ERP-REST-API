from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Index, Integer, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class AcademicPerformance(Base):
    __tablename__ = "academic_performance"
    __table_args__ = (
        Index("ix_perf_student_year_sem", "student_id", "academic_year", "semester"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    semester: Mapped[int] = mapped_column(Integer, nullable=False)
    academic_year: Mapped[str] = mapped_column(String(10), nullable=False, index=True)

    sgpa: Mapped[float | None] = mapped_column(Numeric(4, 2))
    cgpa: Mapped[float | None] = mapped_column(Numeric(4, 2))

    credits_registered: Mapped[int | None] = mapped_column(Integer)
    credits_earned: Mapped[int | None] = mapped_column(Integer)

    backlogs_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    result_status: Mapped[str] = mapped_column(String(20), nullable=False, default="pass")

    class_rank: Mapped[int | None] = mapped_column(Integer)
    department_rank: Mapped[int | None] = mapped_column(Integer)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    student: Mapped["Student"] = relationship("Student", back_populates="performances")
