"""
Placement, internship, higher-studies, and related career services.
"""
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.placement import Placement
from app.models.internship import Internship
from app.models.higher_studies import HigherStudies
from app.models.entrepreneurship import Entrepreneurship
from app.models.publication import Publication
from app.models.professional_activity import ProfessionalActivity
from app.models.award import Award
from app.utils.filters import PLACEMENT_SORT_COLS, INTERNSHIP_SORT_COLS, validate_sort_col
from app.utils.pagination import PaginationParams


def get_placements(
    db: Session,
    pagination: PaginationParams,
    student_id: int | None = None,
    offer_status: str | None = None,
    sort: str = "id",
    order: str = "asc",
):
    sort = validate_sort_col(sort, PLACEMENT_SORT_COLS)
    q = select(Placement)
    if student_id:
        q = q.where(Placement.student_id == student_id)
    if offer_status:
        q = q.where(Placement.offer_status == offer_status)
    col = getattr(Placement, sort)
    q = q.order_by(col.desc() if order == "desc" else col.asc())
    total = db.scalar(select(func.count()).select_from(q.subquery()))
    rows = db.scalars(q.offset(pagination.offset).limit(pagination.limit)).all()
    return rows, total


def get_internships(
    db: Session,
    pagination: PaginationParams,
    student_id: int | None = None,
    sort: str = "id",
    order: str = "asc",
):
    sort = validate_sort_col(sort, INTERNSHIP_SORT_COLS)
    q = select(Internship)
    if student_id:
        q = q.where(Internship.student_id == student_id)
    col = getattr(Internship, sort)
    q = q.order_by(col.desc() if order == "desc" else col.asc())
    total = db.scalar(select(func.count()).select_from(q.subquery()))
    rows = db.scalars(q.offset(pagination.offset).limit(pagination.limit)).all()
    return rows, total


def get_higher_studies(db: Session, pagination: PaginationParams, student_id: int | None = None):
    q = select(HigherStudies)
    if student_id:
        q = q.where(HigherStudies.student_id == student_id)
    total = db.scalar(select(func.count()).select_from(q.subquery()))
    rows = db.scalars(q.offset(pagination.offset).limit(pagination.limit)).all()
    return rows, total


def get_entrepreneurships(db: Session, pagination: PaginationParams, student_id: int | None = None):
    q = select(Entrepreneurship)
    if student_id:
        q = q.where(Entrepreneurship.student_id == student_id)
    total = db.scalar(select(func.count()).select_from(q.subquery()))
    rows = db.scalars(q.offset(pagination.offset).limit(pagination.limit)).all()
    return rows, total


def get_publications(db: Session, pagination: PaginationParams, student_id: int | None = None):
    q = select(Publication)
    if student_id:
        q = q.where(Publication.student_id == student_id)
    total = db.scalar(select(func.count()).select_from(q.subquery()))
    rows = db.scalars(q.offset(pagination.offset).limit(pagination.limit)).all()
    return rows, total


def get_professional_activities(db: Session, pagination: PaginationParams, student_id: int | None = None):
    q = select(ProfessionalActivity)
    if student_id:
        q = q.where(ProfessionalActivity.student_id == student_id)
    total = db.scalar(select(func.count()).select_from(q.subquery()))
    rows = db.scalars(q.offset(pagination.offset).limit(pagination.limit)).all()
    return rows, total


def get_awards(db: Session, pagination: PaginationParams, student_id: int | None = None):
    q = select(Award)
    if student_id:
        q = q.where(Award.student_id == student_id)
    total = db.scalar(select(func.count()).select_from(q.subquery()))
    rows = db.scalars(q.offset(pagination.offset).limit(pagination.limit)).all()
    return rows, total
