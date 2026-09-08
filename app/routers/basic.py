"""
/api/v1/basic/* — HTTP Basic authentication required.
Username: audit_admin  Password: EduPassword@2026
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_basic
from app.schemas.student import StudentOut
from app.schemas.placement import PlacementOut
from app.schemas.higher_studies import HigherStudiesOut
from app.schemas.entrepreneurship import EntrepreneurshipOut
from app.schemas.publication import PublicationOut
from app.schemas.professional_activity import ProfessionalActivityOut
from app.schemas.award import AwardOut
from app.schemas.common import PaginatedResponse
from app.utils.pagination import PaginationParams, make_pagination_meta
from app.services import student_service, placement_service

router = APIRouter(
    prefix="/api/v1/basic",
    tags=["Basic Auth"],
    dependencies=[Depends(require_basic)],
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


@router.get("/placements", response_model=PaginatedResponse[PlacementOut])
def list_placements(
    pagination: PaginationParams = Depends(),
    student_id: int | None = Query(None),
    offer_status: str | None = Query(None),
    sort: str = Query("id"),
    order: str = Query("asc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
):
    rows, total = placement_service.get_placements(db, pagination, student_id, offer_status, sort, order)
    return {"data": rows, "pagination": make_pagination_meta(pagination.page, pagination.limit, total)}


@router.get("/higher-studies", response_model=PaginatedResponse[HigherStudiesOut])
def list_higher_studies(
    pagination: PaginationParams = Depends(),
    student_id: int | None = Query(None),
    db: Session = Depends(get_db),
):
    rows, total = placement_service.get_higher_studies(db, pagination, student_id)
    return {"data": rows, "pagination": make_pagination_meta(pagination.page, pagination.limit, total)}


@router.get("/entrepreneurship", response_model=PaginatedResponse[EntrepreneurshipOut])
def list_entrepreneurship(
    pagination: PaginationParams = Depends(),
    student_id: int | None = Query(None),
    db: Session = Depends(get_db),
):
    rows, total = placement_service.get_entrepreneurships(db, pagination, student_id)
    return {"data": rows, "pagination": make_pagination_meta(pagination.page, pagination.limit, total)}


@router.get("/publications", response_model=PaginatedResponse[PublicationOut])
def list_publications(
    pagination: PaginationParams = Depends(),
    student_id: int | None = Query(None),
    db: Session = Depends(get_db),
):
    rows, total = placement_service.get_publications(db, pagination, student_id)
    return {"data": rows, "pagination": make_pagination_meta(pagination.page, pagination.limit, total)}


@router.get("/professional-activities", response_model=PaginatedResponse[ProfessionalActivityOut])
def list_professional_activities(
    pagination: PaginationParams = Depends(),
    student_id: int | None = Query(None),
    db: Session = Depends(get_db),
):
    rows, total = placement_service.get_professional_activities(db, pagination, student_id)
    return {"data": rows, "pagination": make_pagination_meta(pagination.page, pagination.limit, total)}


@router.get("/awards", response_model=PaginatedResponse[AwardOut])
def list_awards(
    pagination: PaginationParams = Depends(),
    student_id: int | None = Query(None),
    db: Session = Depends(get_db),
):
    rows, total = placement_service.get_awards(db, pagination, student_id)
    return {"data": rows, "pagination": make_pagination_meta(pagination.page, pagination.limit, total)}
