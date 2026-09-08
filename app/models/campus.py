from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Campus(Base):
    __tablename__ = "campuses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    institution_id: Mapped[int] = mapped_column(Integer, ForeignKey("institutions.id"), nullable=False, index=True)
    campus_code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(String(100), nullable=False)
    address: Mapped[str | None] = mapped_column(String(500))
    capacity: Mapped[int | None] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="active")

    institution: Mapped["Institution"] = relationship("Institution", back_populates="campuses")
    departments: Mapped[list["Department"]] = relationship("Department", back_populates="campus")
    students: Mapped[list["Student"]] = relationship("Student", back_populates="campus")
