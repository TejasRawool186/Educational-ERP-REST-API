"""
04_seed_courses.py
------------------
Seeds exactly 350 courses spread across 6 departments and 10 programs.

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

TARGET = 350

COURSE_TYPES = ["theory", "practical", "theory_practical", "elective"]
SUBJECTS = [
    "Data Structures & Algorithms", "Operating Systems", "Database Management Systems",
    "Computer Networks", "Software Engineering", "Machine Learning",
    "Deep Learning", "Cloud Computing", "Cybersecurity", "Web Technologies",
    "Mobile Application Development", "Artificial Intelligence",
    "Natural Language Processing", "Computer Vision", "Embedded Systems",
    "Internet of Things", "Blockchain Technology", "Compiler Design",
    "Engineering Mathematics I", "Engineering Mathematics II",
    "Engineering Physics", "Engineering Chemistry", "Communication Skills",
    "Environmental Science", "Project Management", "Digital Electronics",
    "Microprocessors & Microcontrollers", "VLSI Design", "Signal Processing",
    "Control Systems", "Power Systems", "Electric Machines",
    "Fluid Mechanics", "Thermodynamics", "Strength of Materials",
    "Structural Analysis", "Geotechnical Engineering", "Transportation Engineering",
    "Statistics & Probability", "Linear Algebra", "Numerical Methods",
    "Discrete Mathematics", "Theory of Computation", "Algorithm Design",
    "Big Data Analytics", "Data Warehousing", "Information Security",
    "Human Computer Interaction", "Software Testing", "DevOps Engineering",
]


def seed():
    db = SessionLocal()
    try:
        existing = db.query(Course).count()
        if existing >= TARGET:
            print(f"Courses already seeded ({existing:,}). Skipping.")
            return

        dept_prog_pairs = db.query(Department.id, Program.id).join(
            Program, Program.department_id == Department.id
        ).all()
        if not dept_prog_pairs:
            print("No departments/programs found. Run earlier scripts first.")
            return

        faculty_ids = [r[0] for r in db.query(Faculty.id).all()]

        courses = []
        subject_pool = SUBJECTS * 10   # enough subjects to fill 350 slots
        random.shuffle(subject_pool)

        for i in range(1, TARGET + 1):
            dept_id, prog_id = random.choice(dept_prog_pairs)
            sem = random.randint(1, 8)
            subj = subject_pool[(i - 1) % len(subject_pool)]
            courses.append(Course(
                department_id=dept_id,
                program_id=prog_id,
                course_code=f"CRS{i:05d}",
                course_name=f"{subj}",
                course_type=random.choice(COURSE_TYPES),
                credits=random.choice([2.0, 3.0, 4.0]),
                lecture_hours=random.choice([2, 3]),
                tutorial_hours=random.choice([0, 1]),
                practical_hours=random.choice([0, 2]),
                semester=sem,
                academic_year=f"{2020 + sem // 2}-{2021 + sem // 2}",
                faculty_id=random.choice(faculty_ids) if faculty_ids else None,
                status="active",
            ))

        db.bulk_save_objects(courses)
        db.commit()
        print(f"Course seeding complete — {TARGET} records.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
