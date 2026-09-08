from datetime import date
from sqlalchemy import Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Award(Base):
    __tablename__ = "awards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    faculty_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("faculty.id"), nullable=True, index=True)
    award_name: Mapped[str] = mapped_column(String(300), nullable=False)
    award_category: Mapped[str | None] = mapped_column(String(100))
    awarding_body: Mapped[str | None] = mapped_column(String(200))
    award_date: Mapped[date | None] = mapped_column(Date)
    level: Mapped[str | None] = mapped_column(String(50))       # institute, state, national, international
    position: Mapped[str | None] = mapped_column(String(50))    # 1st, 2nd, 3rd, participant
    description: Mapped[str | None] = mapped_column(Text)

    student: Mapped["Student"] = relationship("Student", back_populates="awards")
    faculty: Mapped["Faculty | None"] = relationship("Faculty")
