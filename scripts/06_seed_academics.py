"""
06_seed_academics.py
--------------------
Seeds enrollments, academic performance, attendance, and examinations
for all students belonging to NextGen Institute of AI & Technology (NGIAT).

IDEMPOTENT — uses enrollment count as guard.
Running this script twice will not create duplicate records.

Courses are matched to the student's own department where possible,
falling back to any available course to ensure realistic FK relationships.

Usage:
    python scripts/06_seed_academics.py
"""
import sys, os, random
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy import select
from app.core.database import SessionLocal
from app.models.student import Student
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.performance import AcademicPerformance
from app.models.attendance import Attendance
from app.models.examination import Examination

random.seed(42)

GRADE_MAP = [
    (9.0, 10.01, "O",  10.0),
    (8.0,  9.0,  "A+",  9.0),
    (7.0,  8.0,  "A",   8.0),
    (6.0,  7.0,  "B+",  7.0),
    (5.0,  6.0,  "B",   6.0),
    (4.0,  5.0,  "C",   5.0),
    (0.0,  4.0,  "F",   0.0),
]

def marks_to_grade(marks_pct: float):
    """Convert 0–100 marks percentage to (grade_letter, grade_point)."""
    v = marks_pct / 10.0
    for lo, hi, g, gp in GRADE_MAP:
        if lo <= v < hi:
            return g, gp
    return "F", 0.0


def seed():
    db = SessionLocal()
    try:
        # ── Idempotency guard ─────────────────────────────────────────────────
        existing_enr = db.query(Enrollment).count()
        if existing_enr > 0:
            print(f"Academics already seeded ({existing_enr:,} enrollments). Skipping.")
            return

        # ── Load students ─────────────────────────────────────────────────────
        student_rows = db.execute(
            select(Student.id, Student.department_id, Student.program_id)
        ).all()
        if not student_rows:
            print("No students found. Run 05_seed_students.py first.")
            return

        # ── Build dept → course_ids index for realistic enrollment ────────────
        course_rows = db.execute(select(Course.id, Course.department_id, Course.semester)).all()
        if not course_rows:
            print("No courses found. Run 04_seed_courses.py first.")
            return

        dept_sem_courses: dict[tuple, list[int]] = defaultdict(list)
        all_course_ids = []
        for cid, dept_id, sem in course_rows:
            dept_sem_courses[(dept_id, sem)].append(cid)
            all_course_ids.append(cid)

        total_students = len(student_rows)
        print(f"Seeding academic records for {total_students:,} students...")

        enr_batch, perf_batch, att_batch, exam_batch = [], [], [], []
        FLUSH_SIZE = 3000

        def flush_all():
            for batch, model_name in [
                (enr_batch,  "enrollments"),
                (perf_batch, "performance"),
                (att_batch,  "attendance"),
                (exam_batch, "examinations"),
            ]:
                if batch:
                    db.bulk_save_objects(batch)
                    batch.clear()
            db.flush()

        for idx, (stu_id, dept_id, prog_id) in enumerate(student_rows, 1):
            sems_completed = random.randint(2, 8)
            cgpa_acc = []

            for sem in range(1, sems_completed + 1):
                academic_year = f"{2019 + sem // 2}-{20 + sem // 2:02d}"

                # Prefer courses from student's own dept+sem, fall back to any
                candidate_courses = (
                    dept_sem_courses.get((dept_id, sem))
                    or dept_sem_courses.get((dept_id, sem % 8 + 1))
                    or all_course_ids
                )
                n_courses = random.randint(4, 7)
                sem_courses = random.sample(
                    candidate_courses, k=min(n_courses, len(candidate_courses))
                )

                sgpa_components = []

                for cid in sem_courses:
                    # Enrollment
                    enr_batch.append(Enrollment(
                        student_id=stu_id,
                        course_id=cid,
                        academic_year=academic_year,
                        semester=sem,
                        enrollment_status="completed",
                    ))

                    # Attendance — slightly right-skewed (most students attend > 75%)
                    conducted = random.randint(40, 65)
                    min_att = max(int(conducted * 0.50), 1)
                    attended = random.randint(min_att, conducted)
                    att_pct = round(attended / conducted * 100, 2)
                    att_batch.append(Attendance(
                        student_id=stu_id,
                        course_id=cid,
                        academic_year=academic_year,
                        semester=sem,
                        classes_conducted=conducted,
                        classes_attended=attended,
                        attendance_percentage=att_pct,
                        status="active",
                    ))

                    # Examination — normally distributed around 65%, clipped 0–100
                    marks = round(max(0.0, min(100.0, random.gauss(65, 18))), 2)
                    grade, gp = marks_to_grade(marks)
                    exam_batch.append(Examination(
                        student_id=stu_id,
                        course_id=cid,
                        exam_type="end-sem",
                        maximum_marks=100.0,
                        marks_obtained=marks,
                        grade=grade,
                        grade_point=gp,
                        result_status="pass" if gp > 0 else "fail",
                    ))
                    sgpa_components.append(gp)

                # Semester performance
                sgpa = round(sum(sgpa_components) / len(sgpa_components), 2) if sgpa_components else 0.0
                cgpa_acc.append(sgpa)
                cgpa = round(sum(cgpa_acc) / len(cgpa_acc), 2)
                backlogs = sum(1 for gp in sgpa_components if gp == 0.0)
                perf_batch.append(AcademicPerformance(
                    student_id=stu_id,
                    semester=sem,
                    academic_year=academic_year,
                    sgpa=sgpa,
                    cgpa=cgpa,
                    credits_registered=len(sem_courses) * 3,
                    credits_earned=max(0, (len(sem_courses) - backlogs)) * 3,
                    backlogs_count=backlogs,
                    result_status="pass" if backlogs == 0 else "fail",
                ))

            # Flush periodically to avoid OOM on large datasets
            if (
                len(enr_batch) >= FLUSH_SIZE
                or len(att_batch) >= FLUSH_SIZE
                or len(exam_batch) >= FLUSH_SIZE
            ):
                flush_all()

            if idx % 2000 == 0:
                flush_all()
                print(f"  {idx:,} / {total_students:,} students processed...")

        # Final flush
        flush_all()
        db.commit()
        print("Academic seeding complete.")
        print(f"  Enrollments  : {db.query(Enrollment).count():,}")
        print(f"  Performance  : {db.query(AcademicPerformance).count():,}")
        print(f"  Attendance   : {db.query(Attendance).count():,}")
        print(f"  Examinations : {db.query(Examination).count():,}")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
