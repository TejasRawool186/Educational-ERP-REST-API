from datetime import date
from sqlalchemy import Boolean, Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class ProfessionalActivity(Base):
    __tablename__ = "professional_activities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    activity_type: Mapped[str] = mapped_column(String(100), nullable=False)  # hackathon, workshop, seminar …
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    organization: Mapped[str | None] = mapped_column(String(200))
    activity_date: Mapped[date | None] = mapped_column(Date)
    role: Mapped[str | None] = mapped_column(String(100))
    outcome: Mapped[str | None] = mapped_column(String(100))
    certificate_available: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    student: Mapped["Student"] = relationship("Student", back_populates="professional_activities")
