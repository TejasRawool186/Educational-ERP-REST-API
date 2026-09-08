"""
Academic performance, attendance, examination services.
"""
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.performance import AcademicPerformance
from app.models.attendance import Attendance
from app.models.examination import Examination
from app.utils.filters import PERFORMANCE_SORT_COLS, validate_sort_col
from app.utils.pagination import PaginationParams


def get_performances(
    db: Session,
    pagination: PaginationParams,
    student_id: int | None = None,
    semester: int | None = None,
    academic_year: str | None = None,
    sort: str = "id",
    order: str = "asc",
):
    sort = validate_sort_col(sort, PERFORMANCE_SORT_COLS)
    q = select(AcademicPerformance)
    if student_id:
        q = q.where(AcademicPerformance.student_id == student_id)
    if semester:
        q = q.where(AcademicPerformance.semester == semester)
    if academic_year:
        q = q.where(AcademicPerformance.academic_year == academic_year)
    col = getattr(AcademicPerformance, sort)
    q = q.order_by(col.desc() if order == "desc" else col.asc())
    total = db.scalar(select(func.count()).select_from(q.subquery()))
    rows = db.scalars(q.offset(pagination.offset).limit(pagination.limit)).all()
    return rows, total


def get_attendances(
    db: Session,
    pagination: PaginationParams,
    student_id: int | None = None,
    course_id: int | None = None,
    sort: str = "id",
    order: str = "asc",
):
    q = select(Attendance)
    if student_id:
        q = q.where(Attendance.student_id == student_id)
    if course_id:
        q = q.where(Attendance.course_id == course_id)
    col = getattr(Attendance, sort) if hasattr(Attendance, sort) else Attendance.id
    q = q.order_by(col.desc() if order == "desc" else col.asc())
    total = db.scalar(select(func.count()).select_from(q.subquery()))
    rows = db.scalars(q.offset(pagination.offset).limit(pagination.limit)).all()
    return rows, total


def get_examinations(
    db: Session,
    pagination: PaginationParams,
    student_id: int | None = None,
    course_id: int | None = None,
    sort: str = "id",
    order: str = "asc",
):
    q = select(Examination)
    if student_id:
        q = q.where(Examination.student_id == student_id)
    if course_id:
        q = q.where(Examination.course_id == course_id)
    col = getattr(Examination, sort) if hasattr(Examination, sort) else Examination.id
    q = q.order_by(col.desc() if order == "desc" else col.asc())
    total = db.scalar(select(func.count()).select_from(q.subquery()))
    rows = db.scalars(q.offset(pagination.offset).limit(pagination.limit)).all()
    return rows, total
