"""
05_seed_students.py
-------------------
Seeds synthetic students for NextGen Institute of AI & Technology (NGIAT).

Dataset size is controlled by environment variables — do not hardcode.

  DATASET_SIZE=small    →   1,000 students
  DATASET_SIZE=medium   →  10,000 students  (default)
  DATASET_SIZE=large    →  50,000 students
  DATASET_SIZE=xl       → 100,000 students

  SEED_STUDENTS=<n>     → exact count (overrides DATASET_SIZE)

Usage:
    python scripts/05_seed_students.py

    # PowerShell examples:
    $env:DATASET_SIZE="large";  python scripts/05_seed_students.py
    $env:SEED_STUDENTS=100000;  python scripts/05_seed_students.py
"""
import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Resolve target before any other imports so config is loaded first
from app.core.config import get_student_target

TARGET = get_student_target()
BATCH_SIZE = 500

from faker import Faker
from app.core.database import SessionLocal
from app.models.student import Student
from app.models.campus import Campus
from app.models.department import Department
from app.models.program import Program
from app.models.institution import Institution

fake = Faker("en_IN")
random.seed(42)
Faker.seed(42)

GENDERS = ["Male", "Female", "Other"]
CATEGORIES = ["General", "OBC", "SC", "ST", "EWS"]
ADMISSION_TYPES = ["CAP", "Direct", "Management", "NRI", "Lateral"]
# Weighted toward active — realistic for a live institution
STATUSES = ["active", "active", "active", "active", "alumni", "dropout"]
# NGIAT founded 2005; B.Tech batches: students admit 4 years before graduation
BATCH_YEARS = list(range(2018, 2026))
STATES = [
    "Maharashtra", "Karnataka", "Tamil Nadu", "Telangana", "Gujarat",
    "Delhi", "Uttar Pradesh", "West Bengal", "Rajasthan", "Punjab",
]


def seed():
    db = SessionLocal()
    try:
        existing = db.query(Student).count()
        if existing >= TARGET:
            print(f"Students already seeded ({existing:,} >= target {TARGET:,}). Skipping.")
            return

        # Only load rows belonging to NGIAT (institution_id=1 for V1)
        rows = (
            db.query(Institution.id, Campus.id, Department.id, Program.id)
            .join(Campus, Campus.institution_id == Institution.id)
            .join(Department, Department.campus_id == Campus.id)
            .join(Program, Program.department_id == Department.id)
            .filter(Institution.institution_code == "NGIAT001")
            .all()
        )

        if not rows:
            print("No NGIAT master data found. Run 02_seed_master.py first.")
            return

        print(f"Seeding {TARGET:,} students for NGIAT (resuming from {existing:,})...")
        students = []
        start = existing + 1

        for i in range(start, TARGET + 1):
            inst_id, camp_id, dept_id, prog_id = random.choice(rows)
            batch = random.choice(BATCH_YEARS)
            first = fake.first_name()
            middle = fake.first_name() if random.random() < 0.4 else None
            last = fake.last_name()
            full = f"{first} {middle + ' ' if middle else ''}{last}"
            state = random.choice(STATES)

            s = Student(
                student_uid=f"NGIAT{i:07d}",
                institution_id=inst_id,
                campus_id=camp_id,
                department_id=dept_id,
                program_id=prog_id,
                roll_number=f"NGIAT{batch}-{i:06d}",
                first_name=first,
                middle_name=middle,
                last_name=last,
                full_name=full,
                gender=random.choice(GENDERS),
                date_of_birth=fake.date_of_birth(minimum_age=17, maximum_age=30),
                category=random.choice(CATEGORIES),
                admission_type=random.choice(ADMISSION_TYPES),
                admission_year=batch,
                batch_year=batch,
                graduation_year=batch + 4,
                current_semester=random.randint(1, 8),
                current_status=random.choice(STATUSES),
                email=f"student{i}@ngiat.edu.in",
                phone=fake.phone_number()[:15],
                city=fake.city(),
                state=state,
                country="India",
            )
            students.append(s)

            if len(students) >= BATCH_SIZE:
                db.bulk_save_objects(students)
                db.flush()
                students = []
                print(f"  {i:,} / {TARGET:,} students seeded...")

        if students:
            db.bulk_save_objects(students)
        db.commit()
        print(f"Student seeding complete — {TARGET:,} total records.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
