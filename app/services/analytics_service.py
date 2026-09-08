"""
Analytics / aggregation queries.
"""
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.student import Student
from app.models.performance import AcademicPerformance
from app.models.placement import Placement
from app.models.attendance import Attendance
from app.models.higher_studies import HigherStudies
from app.models.department import Department


def student_count(db: Session) -> dict:
    total = db.scalar(select(func.count(Student.id)))
    active = db.scalar(select(func.count(Student.id)).where(Student.current_status == "active"))
    rows = db.execute(
        select(Department.name, func.count(Student.id))
        .join(Student, Student.department_id == Department.id)
        .group_by(Department.name)
        .order_by(func.count(Student.id).desc())
    ).all()
    by_dept = [{"department": r[0], "count": r[1]} for r in rows]
    return {"total_students": total, "active_students": active, "by_department": by_dept}


def average_cgpa(db: Session) -> dict:
    overall = db.scalar(select(func.avg(AcademicPerformance.cgpa)))
    rows = db.execute(
        select(Department.name, func.avg(AcademicPerformance.cgpa))
        .join(Student, Student.id == AcademicPerformance.student_id)
        .join(Department, Department.id == Student.department_id)
        .group_by(Department.name)
        .order_by(func.avg(AcademicPerformance.cgpa).desc())
    ).all()
    by_dept = [{"department": r[0], "average_cgpa": round(float(r[1]), 2) if r[1] else None} for r in rows]
    return {
        "overall_average_cgpa": round(float(overall), 2) if overall else 0.0,
        "by_department": by_dept,
    }


def placement_rate(db: Session) -> dict:
    total = db.scalar(select(func.count(Student.id)))
    placed = db.scalar(select(func.count(func.distinct(Placement.student_id))))
    avg_pkg = db.scalar(select(func.avg(Placement.package_lpa)))
    rows = db.execute(
        select(
            Department.name,
            func.count(func.distinct(Student.id)).label("student_count"),
            func.count(func.distinct(Placement.student_id)).label("placed_count"),
        )
        .join(Student, Student.department_id == Department.id)
        .outerjoin(Placement, Placement.student_id == Student.id)
        .group_by(Department.name)
    ).all()
    by_dept = [
        {
            "department": r[0],
            "student_count": r[1],
            "placed_count": r[2],
            "placement_rate": round(r[2] / r[1] * 100, 1) if r[1] else 0.0,
        }
        for r in rows
    ]
    rate = round(placed / total * 100, 1) if total else 0.0
    return {
        "total_students": total,
        "placed_students": placed,
        "placement_rate_percent": rate,
        "average_package_lpa": round(float(avg_pkg), 2) if avg_pkg else None,
        "by_department": by_dept,
    }


def average_package(db: Session) -> dict:
    avg = db.scalar(select(func.avg(Placement.package_lpa)))
    min_ = db.scalar(select(func.min(Placement.package_lpa)))
    max_ = db.scalar(select(func.max(Placement.package_lpa)))
    return {
        "average_package_lpa": round(float(avg), 2) if avg else None,
        "median_package_lpa": None,   # PostgreSQL percentile requires a different query
        "min_package_lpa": round(float(min_), 2) if min_ else None,
        "max_package_lpa": round(float(max_), 2) if max_ else None,
    }


def department_performance(db: Session) -> list[dict]:
    rows = db.execute(
        select(
            Department.id,
            Department.name,
            func.count(func.distinct(Student.id)).label("student_count"),
            func.avg(AcademicPerformance.cgpa).label("avg_cgpa"),
            func.count(func.distinct(Placement.student_id)).label("placed"),
        )
        .join(Student, Student.department_id == Department.id)
        .outerjoin(AcademicPerformance, AcademicPerformance.student_id == Student.id)
        .outerjoin(Placement, Placement.student_id == Student.id)
        .group_by(Department.id, Department.name)
        .order_by(Department.name)
    ).all()
    return [
        {
            "department_id": r[0],
            "department_name": r[1],
            "student_count": r[2],
            "average_cgpa": round(float(r[3]), 2) if r[3] else None,
            "placement_rate": round(r[4] / r[2] * 100, 1) if r[2] else 0.0,
        }
        for r in rows
    ]


def attendance_summary(db: Session) -> dict:
    overall = db.scalar(select(func.avg(Attendance.attendance_percentage)))
    below_75 = db.scalar(
        select(func.count(Attendance.id)).where(Attendance.attendance_percentage < 75)
    )
    rows = db.execute(
        select(Department.name, func.avg(Attendance.attendance_percentage))
        .join(Student, Student.id == Attendance.student_id)
        .join(Department, Department.id == Student.department_id)
        .group_by(Department.name)
    ).all()
    by_dept = [{"department": r[0], "average_attendance": round(float(r[1]), 1) if r[1] else None} for r in rows]
    return {
        "overall_average_attendance": round(float(overall), 1) if overall else 0.0,
        "below_75_percent_count": below_75 or 0,
        "by_department": by_dept,
    }


def higher_studies_summary(db: Session) -> dict:
    total = db.scalar(select(func.count(HigherStudies.id)))
    by_country_rows = db.execute(
        select(HigherStudies.country, func.count(HigherStudies.id))
        .group_by(HigherStudies.country)
        .order_by(func.count(HigherStudies.id).desc())
    ).all()
    by_degree_rows = db.execute(
        select(HigherStudies.degree_type, func.count(HigherStudies.id))
        .group_by(HigherStudies.degree_type)
        .order_by(func.count(HigherStudies.id).desc())
    ).all()
    return {
        "total": total or 0,
        "by_country": [{"country": r[0], "count": r[1]} for r in by_country_rows],
        "by_degree_type": [{"degree_type": r[0], "count": r[1]} for r in by_degree_rows],
    }
