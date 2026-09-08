"""
08_validate_dataset.py
----------------------
Validates the seeded dataset against the integrity checks in the SRS.

Usage:
    python scripts/08_validate_dataset.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy import func, select, text
from app.core.database import SessionLocal
from app.models import *   # noqa: F401,F403


CHECKS = []


def check(name):
    def decorator(fn):
        CHECKS.append((name, fn))
        return fn
    return decorator


@check("Students > 0")
def chk_students(db): return db.scalar(select(func.count(Student.id))) > 0

@check("Departments > 0")
def chk_depts(db): return db.scalar(select(func.count(Department.id))) > 0

@check("Courses > 0")
def chk_courses(db): return db.scalar(select(func.count(Course.id))) > 0

@check("Enrollments > 0")
def chk_enr(db): return db.scalar(select(func.count(Enrollment.id))) > 0

@check("Academic Performance > 0")
def chk_perf(db): return db.scalar(select(func.count(AcademicPerformance.id))) > 0

@check("Placements > 0")
def chk_pl(db): return db.scalar(select(func.count(Placement.id))) > 0

@check("Internships > 0")
def chk_int(db): return db.scalar(select(func.count(Internship.id))) > 0

@check("No orphan enrollments (invalid student_id)")
def chk_orph_enr(db):
    q = text("""
        SELECT COUNT(*) FROM enrollments e
        WHERE NOT EXISTS (SELECT 1 FROM students s WHERE s.id = e.student_id)
    """)
    return db.scalar(q) == 0

@check("No orphan enrollments (invalid course_id)")
def chk_orph_enr_c(db):
    q = text("""
        SELECT COUNT(*) FROM enrollments e
        WHERE NOT EXISTS (SELECT 1 FROM courses c WHERE c.id = e.course_id)
    """)
    return db.scalar(q) == 0

@check("No duplicate student_uid")
def chk_dup_uid(db):
    dup = db.scalar(
        select(func.count()).select_from(
            select(Student.student_uid)
            .group_by(Student.student_uid)
            .having(func.count(Student.student_uid) > 1)
            .subquery()
        )
    )
    return dup == 0

@check("Every student has a valid department_id")
def chk_stu_dept(db):
    q = text("""
        SELECT COUNT(*) FROM students s
        WHERE NOT EXISTS (SELECT 1 FROM departments d WHERE d.id = s.department_id)
    """)
    return db.scalar(q) == 0

@check("Every program has a valid department_id")
def chk_prog_dept(db):
    q = text("""
        SELECT COUNT(*) FROM programs p
        WHERE NOT EXISTS (SELECT 1 FROM departments d WHERE d.id = p.department_id)
    """)
    return db.scalar(q) == 0


def run():
    db = SessionLocal()
    try:
        passed = 0
        failed = 0
        for name, fn in CHECKS:
            try:
                result = fn(db)
                status = "PASS" if result else "FAIL"
                if result:
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                status = f"ERROR: {e}"
                failed += 1
            print(f"  [{status}] {name}")

        print(f"\nResults: {passed} passed, {failed} failed out of {len(CHECKS)} checks.")
        if failed:
            sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    run()
