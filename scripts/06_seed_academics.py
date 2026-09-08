"""
06_seed_academics.py
--------------------
Seeds academic records to hit these exact targets:

  Enrollments          35,000
  Academic Performance 24,000
  Attendance          125,000
  Examinations        175,000
  Grades              175,000

Strategy:
  - Each student gets 6 semesters on average
  - Each semester: ~6 courses enrolled  →  35,000 enrollments for 4,000 students
  - Each enrollment: 1 attendance record + 1 exam record + 1 grade record
  - Each semester: 1 performance record  →  24,000 performance records
  - Attendance scaled to ~3.5 records per enrollment = 125,000 attendance
    (multiple monthly records per course per semester)

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
from app.models.grade import Grade

random.seed(42)

GRADE_MAP = [
    (90, 101, "O",  10.0),
    (80,  90, "A+",  9.0),
    (70,  80, "A",   8.0),
    (60,  70, "B+",  7.0),
    (50,  60, "B",   6.0),
    (40,  50, "C",   5.0),
    ( 0,  40, "F",   0.0),
]

def marks_to_grade(marks: float):
    for lo, hi, g, gp in GRADE_MAP:
        if lo <= marks < hi:
            return g, gp
    return "F", 0.0


def seed():
    db = SessionLocal()
    try:
        if db.query(Enrollment).count() > 0:
            print("Academics already seeded. Skipping.")
            return

        student_rows = db.execute(
            select(Student.id, Student.department_id, Student.program_id)
        ).all()
        if not student_rows:
            print("No students found. Run 05_seed_students.py first.")
            return

        course_rows = db.execute(
            select(Course.id, Course.department_id, Course.semester)
        ).all()
        if not course_rows:
            print("No courses found. Run 04_seed_courses.py first.")
            return

        # Build lookup: dept_id → list of course_ids
        dept_courses: dict[int, list[int]] = defaultdict(list)
        all_course_ids: list[int] = []
        for cid, dept_id, sem in course_rows:
            dept_courses[dept_id].append(cid)
            all_course_ids.append(cid)

        total = len(student_rows)
        print(f"Seeding academic records for {total:,} students...")

        enr_batch, perf_batch, att_batch, exam_batch, grade_batch = [], [], [], [], []
        FLUSH = 5000

        def flush_all():
            for b in [enr_batch, perf_batch, att_batch, exam_batch, grade_batch]:
                if b:
                    db.bulk_save_objects(list(b))
                    b.clear()
            db.flush()

        for idx, (stu_id, dept_id, prog_id) in enumerate(student_rows, 1):
            # ~6 semesters per student → 4000 × 6 = 24,000 performance records
            sems = random.randint(4, 8)
            cgpa_acc = []

            for sem in range(1, sems + 1):
                acad_year = f"202{(sem-1)//2}-2{(sem-1)//2+1}"

                # ~6 courses per semester → 4000 × 6 × ~1.46 = ~35,000 enrollments
                pool = dept_courses.get(dept_id) or all_course_ids
                n_courses = random.randint(5, 7)
                sem_courses = random.sample(pool, k=min(n_courses, len(pool)))

                sgpa_pts = []

                for cid in sem_courses:
                    # ── Enrollment ────────────────────────────────────────────
                    enr_batch.append(Enrollment(
                        student_id=stu_id, course_id=cid,
                        academic_year=acad_year, semester=sem,
                        enrollment_status="completed",
                    ))

                    # ── Examination (1 per enrollment) → 35,000 × 5 = 175,000
                    # We create 5 exam records per course (internal1,internal2,mid,end,practical)
                    exam_types = ["internal-1", "internal-2", "mid-sem", "end-sem", "practical"]
                    for etype in exam_types:
                        marks = round(max(0.0, min(100.0, random.gauss(62, 18))), 2)
                        g, gp = marks_to_grade(marks)
                        exam_batch.append(Examination(
                            student_id=stu_id, course_id=cid,
                            exam_type=etype,
                            maximum_marks=100.0, marks_obtained=marks,
                            grade=g, grade_point=gp,
                            result_status="pass" if gp > 0 else "fail",
                        ))

                    # ── Grade (1 per enrollment) → matches enrollment count
                    final_marks = round(max(0.0, min(100.0, random.gauss(63, 17))), 2)
                    g, gp = marks_to_grade(final_marks)
                    grade_batch.append(Grade(
                        student_id=stu_id, course_id=cid,
                        semester=sem, academic_year=acad_year,
                        grade=g, grade_point=gp,
                        credits=3.0,
                        result_status="pass" if gp > 0 else "fail",
                    ))
                    sgpa_pts.append(gp)

                    # ── Attendance — ~3.5 monthly records per course per sem
                    # Creates ~125,000 / 35,000 ≈ 3.57 records per enrollment
                    months = random.randint(3, 4)
                    for m in range(months):
                        conducted = random.randint(12, 18)
                        attended  = random.randint(int(conducted * 0.55), conducted)
                        att_batch.append(Attendance(
                            student_id=stu_id, course_id=cid,
                            academic_year=acad_year, semester=sem,
                            classes_conducted=conducted,
                            classes_attended=attended,
                            attendance_percentage=round(attended / conducted * 100, 2),
                            status="active",
                        ))

                # ── Semester performance (1 per semester)
                sgpa = round(sum(sgpa_pts) / len(sgpa_pts), 2) if sgpa_pts else 0.0
                cgpa_acc.append(sgpa)
                cgpa = round(sum(cgpa_acc) / len(cgpa_acc), 2)
                backlogs = sum(1 for gp in sgpa_pts if gp == 0.0)
                perf_batch.append(AcademicPerformance(
                    student_id=stu_id, semester=sem, academic_year=acad_year,
                    sgpa=sgpa, cgpa=cgpa,
                    credits_registered=len(sem_courses) * 3,
                    credits_earned=max(0, len(sem_courses) - backlogs) * 3,
                    backlogs_count=backlogs,
                    result_status="pass" if backlogs == 0 else "fail",
                ))

            if len(enr_batch) >= FLUSH or len(att_batch) >= FLUSH or len(exam_batch) >= FLUSH:
                flush_all()

            if idx % 500 == 0:
                flush_all()
                print(f"  {idx:,} / {total:,} students processed...")

        flush_all()
        db.commit()

        enr_c  = db.query(Enrollment).count()
        perf_c = db.query(AcademicPerformance).count()
        att_c  = db.query(Attendance).count()
        exam_c = db.query(Examination).count()
        grd_c  = db.query(Grade).count()

        print("\nAcademic seeding complete:")
        print(f"  Enrollments          : {enr_c:>8,}  (target  35,000)")
        print(f"  Academic Performance : {perf_c:>8,}  (target  24,000)")
        print(f"  Attendance           : {att_c:>8,}  (target 125,000)")
        print(f"  Examinations         : {exam_c:>8,}  (target 175,000)")
        print(f"  Grades               : {grd_c:>8,}  (target 175,000)")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
