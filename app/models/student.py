from datetime import date, datetime
from sqlalchemy import Date, DateTime, ForeignKey, Index, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Student(Base):
    __tablename__ = "students"
    __table_args__ = (
        Index("ix_students_dept_batch", "department_id", "batch_year"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_uid: Mapped[str] = mapped_column(String(30), unique=True, nullable=False, index=True)
    institution_id: Mapped[int] = mapped_column(Integer, ForeignKey("institutions.id"), nullable=False)
    campus_id: Mapped[int] = mapped_column(Integer, ForeignKey("campuses.id"), nullable=False, index=True)
    department_id: Mapped[int] = mapped_column(Integer, ForeignKey("departments.id"), nullable=False, index=True)
    program_id: Mapped[int] = mapped_column(Integer, ForeignKey("programs.id"), nullable=False, index=True)

    roll_number: Mapped[str] = mapped_column(String(30), unique=True, nullable=False, index=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    middle_name: Mapped[str | None] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    full_name: Mapped[str] = mapped_column(String(300), nullable=False)

    gender: Mapped[str | None] = mapped_column(String(20))
    date_of_birth: Mapped[date | None] = mapped_column(Date)

    category: Mapped[str | None] = mapped_column(String(50))       # General, OBC, SC, ST …
    admission_type: Mapped[str | None] = mapped_column(String(50)) # CAP, Direct, Management …

    admission_year: Mapped[int] = mapped_column(Integer, nullable=False)
    batch_year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    graduation_year: Mapped[int | None] = mapped_column(Integer)

    current_semester: Mapped[int | None] = mapped_column(Integer)
    current_status: Mapped[str] = mapped_column(String(30), nullable=False, default="active")

    email: Mapped[str | None] = mapped_column(String(200))
    phone: Mapped[str | None] = mapped_column(String(20))

    city: Mapped[str | None] = mapped_column(String(100))
    state: Mapped[str | None] = mapped_column(String(100))
    country: Mapped[str] = mapped_column(String(100), nullable=False, default="India")

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    campus: Mapped["Campus"] = relationship("Campus", back_populates="students")
    department: Mapped["Department"] = relationship("Department", back_populates="students")
    program: Mapped["Program"] = relationship("Program", back_populates="students")
    enrollments: Mapped[list["Enrollment"]] = relationship("Enrollment", back_populates="student")
    performances: Mapped[list["AcademicPerformance"]] = relationship("AcademicPerformance", back_populates="student")
    attendances: Mapped[list["Attendance"]] = relationship("Attendance", back_populates="student")
    examinations: Mapped[list["Examination"]] = relationship("Examination", back_populates="student")
    grades: Mapped[list["Grade"]] = relationship("Grade", back_populates="student")
    internships: Mapped[list["Internship"]] = relationship("Internship", back_populates="student")
    placements: Mapped[list["Placement"]] = relationship("Placement", back_populates="student")
    higher_studies: Mapped[list["HigherStudies"]] = relationship("HigherStudies", back_populates="student")
    entrepreneurships: Mapped[list["Entrepreneurship"]] = relationship("Entrepreneurship", back_populates="student")
    projects: Mapped[list["Project"]] = relationship("Project", back_populates="student")
    certifications: Mapped[list["Certification"]] = relationship("Certification", back_populates="student")
    publications: Mapped[list["Publication"]] = relationship("Publication", back_populates="student")
    professional_activities: Mapped[list["ProfessionalActivity"]] = relationship("ProfessionalActivity", back_populates="student")
    awards: Mapped[list["Award"]] = relationship("Award", back_populates="student")
