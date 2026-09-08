"""
/api/v1/apikey/* — API key header authentication required.
X-API-Key: EDU-APIKEY-2026
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_api_key
from app.models.student import Student
from app.models.faculty import Faculty
from app.models.enrollment import Enrollment
from app.models.course import Course
from app.models.internship import Internship
from app.models.project import Project
from app.models.certification import Certification
from app.schemas.student import StudentOut
from app.schemas.faculty import FacultyOut
from app.schemas.enrollment import EnrollmentOut
from app.schemas.course import CourseOut
from app.schemas.internship import InternshipOut
from app.schemas.project import ProjectOut
from app.schemas.certification import CertificationOut
from app.schemas.common import PaginatedResponse
from app.utils.pagination import PaginationParams, make_pagination_meta
from app.utils.filters import (
    STUDENT_SORT_COLS, FACULTY_SORT_COLS, COURSE_SORT_COLS,
    INTERNSHIP_SORT_COLS, CERTIFICATION_SORT_COLS, PROJECT_SORT_COLS,
    validate_sort_col,
)
from app.services import student_service, placement_service

router = APIRouter(
    prefix="/api/v1/apikey",
    tags=["API Key Auth"],
    dependencies=[Depends(require_api_key)],
)


@router.get("/students", response_model=PaginatedResponse[StudentOut])
def list_students(
    pagination: PaginationParams = Depends(),
    department_id: int | None = Query(None),
    batch_year: int | None = Query(None),
    status: str | None = Query(None),
    search: str | None = Query(None),
    sort: str = Query("id"),
    order: str = Query("asc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
):
    rows, total = student_service.get_students(
        db, pagination, department_id, None, batch_year, status, search, sort, order
    )
    return {"data": rows, "pagination": make_pagination_meta(pagination.page, pagination.limit, total)}


@router.get("/faculty", response_model=PaginatedResponse[FacultyOut])
def list_faculty(
    pagination: PaginationParams = Depends(),
    department_id: int | None = Query(None),
    sort: str = Query("id"),
    order: str = Query("asc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
):
    sort = validate_sort_col(sort, FACULTY_SORT_COLS)
    q = select(Faculty)
    if department_id:
        q = q.where(Faculty.department_id == department_id)
    col = getattr(Faculty, sort)
    q = q.order_by(col.desc() if order == "desc" else col.asc())
    total = db.scalar(select(func.count()).select_from(q.subquery()))
    rows = db.scalars(q.offset(pagination.offset).limit(pagination.limit)).all()
    return {"data": rows, "pagination": make_pagination_meta(pagination.page, pagination.limit, total)}


@router.get("/enrollments", response_model=PaginatedResponse[EnrollmentOut])
def list_enrollments(
    pagination: PaginationParams = Depends(),
    student_id: int | None = Query(None),
    course_id: int | None = Query(None),
    db: Session = Depends(get_db),
):
    q = select(Enrollment)
    if student_id:
        q = q.where(Enrollment.student_id == student_id)
    if course_id:
        q = q.where(Enrollment.course_id == course_id)
    total = db.scalar(select(func.count()).select_from(q.subquery()))
    rows = db.scalars(q.offset(pagination.offset).limit(pagination.limit)).all()
    return {"data": rows, "pagination": make_pagination_meta(pagination.page, pagination.limit, total)}


@router.get("/courses", response_model=PaginatedResponse[CourseOut])
def list_courses(
    pagination: PaginationParams = Depends(),
    department_id: int | None = Query(None),
    semester: int | None = Query(None),
    sort: str = Query("id"),
    order: str = Query("asc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
):
    sort = validate_sort_col(sort, COURSE_SORT_COLS)
    q = select(Course)
    if department_id:
        q = q.where(Course.department_id == department_id)
    if semester:
        q = q.where(Course.semester == semester)
    col = getattr(Course, sort)
    q = q.order_by(col.desc() if order == "desc" else col.asc())
    total = db.scalar(select(func.count()).select_from(q.subquery()))
    rows = db.scalars(q.offset(pagination.offset).limit(pagination.limit)).all()
    return {"data": rows, "pagination": make_pagination_meta(pagination.page, pagination.limit, total)}


@router.get("/internships", response_model=PaginatedResponse[InternshipOut])
def list_internships(
    pagination: PaginationParams = Depends(),
    student_id: int | None = Query(None),
    db: Session = Depends(get_db),
):
    rows, total = placement_service.get_internships(db, pagination, student_id)
    return {"data": rows, "pagination": make_pagination_meta(pagination.page, pagination.limit, total)}


@router.get("/projects", response_model=PaginatedResponse[ProjectOut])
def list_projects(
    pagination: PaginationParams = Depends(),
    student_id: int | None = Query(None),
    db: Session = Depends(get_db),
):
    from app.models.project import Project as ProjectModel
    q = select(ProjectModel)
    if student_id:
        q = q.where(ProjectModel.student_id == student_id)
    total = db.scalar(select(func.count()).select_from(q.subquery()))
    rows = db.scalars(q.offset(pagination.offset).limit(pagination.limit)).all()
    return {"data": rows, "pagination": make_pagination_meta(pagination.page, pagination.limit, total)}


@router.get("/certifications", response_model=PaginatedResponse[CertificationOut])
def list_certifications(
    pagination: PaginationParams = Depends(),
    student_id: int | None = Query(None),
    db: Session = Depends(get_db),
):
    from app.models.certification import Certification as CertModel
    q = select(CertModel)
    if student_id:
        q = q.where(CertModel.student_id == student_id)
    total = db.scalar(select(func.count()).select_from(q.subquery()))
    rows = db.scalars(q.offset(pagination.offset).limit(pagination.limit)).all()
    return {"data": rows, "pagination": make_pagination_meta(pagination.page, pagination.limit, total)}
