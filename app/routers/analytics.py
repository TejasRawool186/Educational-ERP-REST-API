"""
/api/v1/bearer/analytics/* — aggregation endpoints, Bearer auth required.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_bearer
from app.services import analytics_service

router = APIRouter(
    prefix="/api/v1/bearer/analytics",
    tags=["Analytics"],
    dependencies=[Depends(require_bearer)],
)


@router.get("/student-count", summary="Total student count and breakdown by department")
def student_count(db: Session = Depends(get_db)):
    return analytics_service.student_count(db)


@router.get("/average-cgpa", summary="Average CGPA overall and by department")
def avg_cgpa(db: Session = Depends(get_db)):
    return analytics_service.average_cgpa(db)


@router.get("/placement-rate", summary="Placement rate overall and by department")
def placement_rate(db: Session = Depends(get_db)):
    return analytics_service.placement_rate(db)


@router.get("/average-package", summary="Package statistics (LPA)")
def avg_package(db: Session = Depends(get_db)):
    return analytics_service.average_package(db)


@router.get("/department-performance", summary="Per-department performance summary")
def dept_performance(db: Session = Depends(get_db)):
    return analytics_service.department_performance(db)


@router.get("/attendance-summary", summary="Attendance summary overall and by department")
def attendance_summary(db: Session = Depends(get_db)):
    return analytics_service.attendance_summary(db)


@router.get("/higher-studies", summary="Higher studies summary by country and degree type")
def higher_studies(db: Session = Depends(get_db)):
    return analytics_service.higher_studies_summary(db)
