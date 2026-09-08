"""
04_seed_courses.py
------------------
Seeds ~5,000 synthetic courses.

Usage:
    python scripts/04_seed_courses.py
"""
import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.core.database import SessionLocal
from app.models.course import Course
from app.models.department import Department
from app.models.program import Program
from app.models.faculty import Faculty

random.seed(42)

COURSE_TYPES = ["theory", "practical", "theory_practical", "elective", "audit"]
SUBJECTS = [
    "Data Structures", "Algorithms", "Operating Systems", "Database Management",
    "Computer Networks", "Software Engineering", "Machine Learning", "Deep Learning",
    "Cloud Computing", "Cybersecurity", "Web Development", "Mobile Computing",
    "Artificial Intelligence", "Natural Language Processing", "Computer Vision",
    "Embedded Systems", "IoT", "Blockchain", "Compiler Design", "Theory of Computation",
    "Engineering Mathematics", "Engineering Physics", "Engineering Chemistry",
    "Communication Skills", "Environmental Science", "Project Management",
    "Digital Electronics", "Microprocessors", "VLSI Design", "Signal Processing",
]
BATCH_SIZE = 500
TARGET = 5000


def seed():
    db = SessionLocal()
    try:
        if db.query(Course).count() >= TARGET:
            print("Courses already seeded. Skipping.")
            return

        dept_prog_pairs = db.query(Department.id, Program.id).join(
            Program, Program.department_id == Department.id
        ).all()
        if not dept_prog_pairs:
            print("No departments/programs. Run earlier scripts first.")
            return

        faculty_ids = [r[0] for r in db.query(Faculty.id).all()]
        courses = []
        course_num = 1
        while course_num <= TARGET:
            for dept_id, prog_id in dept_prog_pairs:
                if course_num > TARGET:
                    break
                subj = random.choice(SUBJECTS)
                sem = random.randint(1, 8)
                c = Course(
                    department_id=dept_id,
                    program_id=prog_id,
                    course_code=f"CRS{course_num:06d}",
                    course_name=f"{subj} {course_num}",
                    course_type=random.choice(COURSE_TYPES),
                    credits=random.choice([1.0, 2.0, 3.0, 4.0]),
                    lecture_hours=random.choice([2, 3, 4]),
                    tutorial_hours=random.choice([0, 1]),
                    practical_hours=random.choice([0, 2, 3]),
                    semester=sem,
                    academic_year=f"{2020 + sem // 2}-{2021 + sem // 2}",
                    faculty_id=random.choice(faculty_ids) if faculty_ids else None,
                    status="active",
                )
                courses.append(c)
                course_num += 1
                if len(courses) >= BATCH_SIZE:
                    db.bulk_save_objects(courses)
                    db.flush()
                    courses = []
                    print(f"  {course_num - 1:,} courses seeded...")

        if courses:
            db.bulk_save_objects(courses)
        db.commit()
        print(f"Course seeding complete — {TARGET:,} records.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
