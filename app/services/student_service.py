"""
Student CRUD / query service.
"""
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models.student import Student
from app.models.performance import AcademicPerformance
from app.models.attendance import Attendance
from app.models.placement import Placement
from app.models.internship import Internship
from app.models.project import Project
from app.utils.filters import STUDENT_SORT_COLS, validate_sort_col
from app.utils.pagination import PaginationParams


def get_students(
    db: Session,
    pagination: PaginationParams,
    department_id: int | None = None,
    program_id: int | None = None,
    batch_year: int | None = None,
    status: str | None = None,
    search: str | None = None,
    sort: str = "id",
    order: str = "asc",
):
    sort = validate_sort_col(sort, STUDENT_SORT_COLS)
    q = select(Student)

    if department_id:
        q = q.where(Student.department_id == department_id)
    if program_id:
        q = q.where(Student.program_id == program_id)
    if batch_year:
        q = q.where(Student.batch_year == batch_year)
    if status:
        q = q.where(Student.current_status == status)
    if search:
        pattern = f"%{search}%"
        q = q.where(
            or_(
                Student.full_name.ilike(pattern),
                Student.first_name.ilike(pattern),
                Student.last_name.ilike(pattern),
                Student.student_uid.ilike(pattern),
                Student.roll_number.ilike(pattern),
            )
        )

    col = getattr(Student, sort)
    q = q.order_by(col.desc() if order == "desc" else col.asc())

    total = db.scalar(select(func.count()).select_from(q.subquery()))
    rows = db.scalars(q.offset(pagination.offset).limit(pagination.limit)).all()
    return rows, total


def get_student_by_id(db: Session, student_id: int) -> Student | None:
    return db.get(Student, student_id)


def get_student_performance(db: Session, student_id: int) -> list[AcademicPerformance]:
    return db.scalars(
        select(AcademicPerformance)
        .where(AcademicPerformance.student_id == student_id)
        .order_by(AcademicPerformance.semester)
    ).all()


def get_student_attendance(db: Session, student_id: int) -> list[Attendance]:
    return db.scalars(
        select(Attendance).where(Attendance.student_id == student_id)
    ).all()


def get_student_placements(db: Session, student_id: int) -> list[Placement]:
    return db.scalars(
        select(Placement).where(Placement.student_id == student_id)
    ).all()


def get_student_internships(db: Session, student_id: int) -> list[Internship]:
    return db.scalars(
        select(Internship).where(Internship.student_id == student_id)
    ).all()


def get_student_projects(db: Session, student_id: int) -> list[Project]:
    return db.scalars(
        select(Project).where(Project.student_id == student_id)
    ).all()
