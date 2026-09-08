"""
/api/v1/public/* — no authentication required.
Exposes master/reference data for NextGen Institute of AI & Technology (NGIAT).

Endpoints:
  /institution   — single-institution view (NGIAT, id=1)
  /institutions  — paginated list (kept for future multi-institution support)
  /campuses
  /departments
  /programs
  /courses
  /faculty
"""
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.institution import Institution
from app.models.campus import Campus
from app.models.department import Department
from app.models.program import Program
from app.models.course import Course
from app.models.faculty import Faculty
from app.schemas.institution import InstitutionOut
from app.schemas.campus import CampusOut
from app.schemas.department import DepartmentOut
from app.schemas.program import ProgramOut
from app.schemas.course import CourseOut
from app.schemas.faculty import FacultyOut
from app.schemas.common import PaginatedResponse, SingleResponse
from app.utils.pagination import PaginationParams, make_pagination_meta
from app.utils.errors import not_found

router = APIRouter(prefix="/api/v1/public", tags=["Public"])


@router.get(
    "/institution",
    response_model=SingleResponse[InstitutionOut],
    summary="Get NextGen Institute of AI & Technology",
)
def get_institution(db: Session = Depends(get_db)):
    """
    Returns the single institution record for NextGen Institute of AI & Technology (NGIAT).
    Version 1 always returns institution_id = 1.
    The institution_id architecture is preserved for future multi-institution support.
    """
    inst = db.scalar(
        select(Institution).where(Institution.institution_code == "NGIAT001")
    )
    if not inst:
        raise not_found("Institution")
    return {"data": inst}


@router.get(
    "/institutions",
    response_model=PaginatedResponse[InstitutionOut],
    summary="List institutions (paginated — kept for future multi-institution support)",
)
def list_institutions(pagination: PaginationParams = Depends(), db: Session = Depends(get_db)):
    q = select(Institution).order_by(Institution.id)
    total = db.scalar(select(func.count()).select_from(q.subquery()))
    rows = db.scalars(q.offset(pagination.offset).limit(pagination.limit)).all()
    return {"data": rows, "pagination": make_pagination_meta(pagination.page, pagination.limit, total)}


@router.get("/campuses", response_model=PaginatedResponse[CampusOut])
def list_campuses(pagination: PaginationParams = Depends(), db: Session = Depends(get_db)):
    q = select(Campus).order_by(Campus.id)
    total = db.scalar(select(func.count()).select_from(q.subquery()))
    rows = db.scalars(q.offset(pagination.offset).limit(pagination.limit)).all()
    return {"data": rows, "pagination": make_pagination_meta(pagination.page, pagination.limit, total)}


@router.get("/departments", response_model=PaginatedResponse[DepartmentOut])
def list_departments(pagination: PaginationParams = Depends(), db: Session = Depends(get_db)):
    q = select(Department).order_by(Department.id)
    total = db.scalar(select(func.count()).select_from(q.subquery()))
    rows = db.scalars(q.offset(pagination.offset).limit(pagination.limit)).all()
    return {"data": rows, "pagination": make_pagination_meta(pagination.page, pagination.limit, total)}


@router.get("/programs", response_model=PaginatedResponse[ProgramOut])
def list_programs(pagination: PaginationParams = Depends(), db: Session = Depends(get_db)):
    q = select(Program).order_by(Program.id)
    total = db.scalar(select(func.count()).select_from(q.subquery()))
    rows = db.scalars(q.offset(pagination.offset).limit(pagination.limit)).all()
    return {"data": rows, "pagination": make_pagination_meta(pagination.page, pagination.limit, total)}


@router.get("/courses", response_model=PaginatedResponse[CourseOut])
def list_courses(pagination: PaginationParams = Depends(), db: Session = Depends(get_db)):
    q = select(Course).order_by(Course.id)
    total = db.scalar(select(func.count()).select_from(q.subquery()))
    rows = db.scalars(q.offset(pagination.offset).limit(pagination.limit)).all()
    return {"data": rows, "pagination": make_pagination_meta(pagination.page, pagination.limit, total)}


@router.get("/faculty", response_model=PaginatedResponse[FacultyOut])
def list_faculty(pagination: PaginationParams = Depends(), db: Session = Depends(get_db)):
    q = select(Faculty).order_by(Faculty.id)
    total = db.scalar(select(func.count()).select_from(q.subquery()))
    rows = db.scalars(q.offset(pagination.offset).limit(pagination.limit)).all()
    return {"data": rows, "pagination": make_pagination_meta(pagination.page, pagination.limit, total)}
