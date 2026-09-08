from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class HigherStudies(Base):
    __tablename__ = "higher_studies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    institution_name: Mapped[str] = mapped_column(String(300), nullable=False)
    country: Mapped[str | None] = mapped_column(String(100))
    program: Mapped[str | None] = mapped_column(String(200))
    degree_type: Mapped[str | None] = mapped_column(String(50))
    specialization: Mapped[str | None] = mapped_column(String(200))
    admission_year: Mapped[int | None] = mapped_column(Integer)
    graduation_year: Mapped[int | None] = mapped_column(Integer)
    scholarship: Mapped[str | None] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="pursuing")

    student: Mapped["Student"] = relationship("Student", back_populates="higher_studies")
