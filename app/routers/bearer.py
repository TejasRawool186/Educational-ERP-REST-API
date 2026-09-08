"""
/api/v1/bearer/* — Bearer token authentication required.
Authorization: Bearer EDU-BEARER-2026
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_bearer
from app.schemas.student import StudentOut
from app.schemas.performance import PerformanceOut
from app.schemas.attendance import AttendanceOut
from app.schemas.placement import PlacementOut
from app.schemas.internship import InternshipOut
from app.schemas.project import ProjectOut
from app.schemas.common import PaginatedResponse, SingleResponse
from app.utils.pagination import PaginationParams, make_pagination_meta
from app.utils.errors import not_found
from app.services import student_service, academic_service

router = APIRouter(
    prefix="/api/v1/bearer",
    tags=["Bearer Auth"],
    dependencies=[Depends(require_bearer)],
)


# ── Students ──────────────────────────────────────────────────────────────────

@router.get("/students", response_model=PaginatedResponse[StudentOut])
def list_students(
    pagination: PaginationParams = Depends(),
    department_id: int | None = Query(None),
    program_id: int | None = Query(None),
    batch_year: int | None = Query(None),
    status: str | None = Query(None),
    search: str | None = Query(None, description="Search by name, UID, or roll number"),
    sort: str = Query("id"),
    order: str = Query("asc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
):
    rows, total = student_service.get_students(
        db, pagination, department_id, program_id, batch_year, status, search, sort, order
    )
    return {"data": rows, "pagination": make_pagination_meta(pagination.page, pagination.limit, total)}


@router.get("/students/{student_id}", response_model=SingleResponse[StudentOut])
def get_student(student_id: int, db: Session = Depends(get_db)):
    s = student_service.get_student_by_id(db, student_id)
    if not s:
        raise not_found("Student")
    return {"data": s}


@router.get("/students/{student_id}/performance", response_model=dict)
def student_performance(student_id: int, db: Session = Depends(get_db)):
    s = student_service.get_student_by_id(db, student_id)
    if not s:
        raise not_found("Student")
    perf = student_service.get_student_performance(db, student_id)
    return {
        "student_id": s.student_uid,
        "performance": [
            {"semester": p.semester, "sgpa": float(p.sgpa) if p.sgpa else None,
             "cgpa": float(p.cgpa) if p.cgpa else None}
            for p in perf
        ],
    }


@router.get("/students/{student_id}/attendance", response_model=dict)
def student_attendance(student_id: int, db: Session = Depends(get_db)):
    s = student_service.get_student_by_id(db, student_id)
    if not s:
        raise not_found("Student")
    att = student_service.get_student_attendance(db, student_id)
    return {"student_id": s.student_uid, "attendance": [AttendanceOut.model_validate(a).model_dump() for a in att]}


@router.get("/students/{student_id}/placements", response_model=dict)
def student_placements(student_id: int, db: Session = Depends(get_db)):
    s = student_service.get_student_by_id(db, student_id)
    if not s:
        raise not_found("Student")
    pl = student_service.get_student_placements(db, student_id)
    return {"student_id": s.student_uid, "placements": [PlacementOut.model_validate(p).model_dump() for p in pl]}


@router.get("/students/{student_id}/internships", response_model=dict)
def student_internships(student_id: int, db: Session = Depends(get_db)):
    s = student_service.get_student_by_id(db, student_id)
    if not s:
        raise not_found("Student")
    interns = student_service.get_student_internships(db, student_id)
    return {"student_id": s.student_uid, "internships": [InternshipOut.model_validate(i).model_dump() for i in interns]}


@router.get("/students/{student_id}/projects", response_model=dict)
def student_projects(student_id: int, db: Session = Depends(get_db)):
    s = student_service.get_student_by_id(db, student_id)
    if not s:
        raise not_found("Student")
    projs = student_service.get_student_projects(db, student_id)
    return {"student_id": s.student_uid, "projects": [ProjectOut.model_validate(p).model_dump() for p in projs]}


# ── Aggregate collections ─────────────────────────────────────────────────────

@router.get("/academic-performance", response_model=PaginatedResponse[PerformanceOut])
def list_performance(
    pagination: PaginationParams = Depends(),
    student_id: int | None = Query(None),
    semester: int | None = Query(None),
    academic_year: str | None = Query(None),
    sort: str = Query("id"),
    order: str = Query("asc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
):
    rows, total = academic_service.get_performances(db, pagination, student_id, semester, academic_year, sort, order)
    return {"data": rows, "pagination": make_pagination_meta(pagination.page, pagination.limit, total)}


@router.get("/attendance", response_model=PaginatedResponse[AttendanceOut])
def list_attendance(
    pagination: PaginationParams = Depends(),
    student_id: int | None = Query(None),
    course_id: int | None = Query(None),
    db: Session = Depends(get_db),
):
    rows, total = academic_service.get_attendances(db, pagination, student_id, course_id)
    return {"data": rows, "pagination": make_pagination_meta(pagination.page, pagination.limit, total)}


@router.get("/examinations", response_model=dict)
def list_examinations(
    pagination: PaginationParams = Depends(),
    student_id: int | None = Query(None),
    course_id: int | None = Query(None),
    db: Session = Depends(get_db),
):
    rows, total = academic_service.get_examinations(db, pagination, student_id, course_id)
    return {
        "data": [
            {
                "id": e.id, "student_id": e.student_id, "course_id": e.course_id,
                "exam_type": e.exam_type, "marks_obtained": float(e.marks_obtained),
                "maximum_marks": float(e.maximum_marks), "grade": e.grade,
                "grade_point": float(e.grade_point) if e.grade_point else None,
                "result_status": e.result_status,
            }
            for e in rows
        ],
        "pagination": make_pagination_meta(pagination.page, pagination.limit, total),
    }
