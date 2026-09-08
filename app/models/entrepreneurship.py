from sqlalchemy import ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Entrepreneurship(Base):
    __tablename__ = "entrepreneurship"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    startup_name: Mapped[str] = mapped_column(String(200), nullable=False)
    startup_type: Mapped[str | None] = mapped_column(String(50))
    industry: Mapped[str | None] = mapped_column(String(100))
    founding_year: Mapped[int | None] = mapped_column(Integer)
    role: Mapped[str | None] = mapped_column(String(100))
    funding_stage: Mapped[str | None] = mapped_column(String(50))
    funding_amount: Mapped[float | None] = mapped_column(Numeric(15, 2))
    employees: Mapped[int | None] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="active")

    student: Mapped["Student"] = relationship("Student", back_populates="entrepreneurships")
