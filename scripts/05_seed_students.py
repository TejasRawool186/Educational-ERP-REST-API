"""
05_seed_students.py
-------------------
Seeds exactly 4,000 students for NextGen Institute of AI & Technology (NGIAT).

Target: 4,000 students
Controlled via SEED_STUDENTS env var if you want a different number.

Usage:
    python scripts/05_seed_students.py
"""
import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

TARGET = int(os.getenv("SEED_STUDENTS", "4000"))
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

GENDERS          = ["Male", "Female", "Other"]
CATEGORIES       = ["General", "OBC", "SC", "ST", "EWS"]
ADMISSION_TYPES  = ["CAP", "Direct", "Management", "Lateral"]
STATUSES         = ["active", "active", "active", "alumni", "dropout"]
BATCH_YEARS      = list(range(2019, 2026))
STATES           = [
    "Maharashtra", "Karnataka", "Tamil Nadu", "Telangana", "Gujarat",
    "Delhi", "Uttar Pradesh", "West Bengal", "Rajasthan", "Punjab",
]


def seed():
    db = SessionLocal()
    try:
        existing = db.query(Student).count()
        if existing >= TARGET:
            print(f"Students already seeded ({existing:,} >= {TARGET:,}). Skipping.")
            return

        rows = (
            db.query(Institution.id, Campus.id, Department.id, Program.id)
            .join(Campus,     Campus.institution_id  == Institution.id)
            .join(Department, Department.campus_id   == Campus.id)
            .join(Program,    Program.department_id  == Department.id)
            .filter(Institution.institution_code == "NGIAT001")
            .all()
        )
        if not rows:
            print("No NGIAT master data found. Run 02_seed_master.py first.")
            return

        print(f"Seeding {TARGET:,} students (resuming from {existing:,})...")
        students = []
        start = existing + 1

        for i in range(start, TARGET + 1):
            inst_id, camp_id, dept_id, prog_id = random.choice(rows)
            batch = random.choice(BATCH_YEARS)
            first  = fake.first_name()
            middle = fake.first_name() if random.random() < 0.35 else None
            last   = fake.last_name()
            full   = f"{first} {middle + ' ' if middle else ''}{last}"

            students.append(Student(
                student_uid     = f"NGIAT{i:06d}",
                institution_id  = inst_id,
                campus_id       = camp_id,
                department_id   = dept_id,
                program_id      = prog_id,
                roll_number     = f"NGIAT{batch}-{i:05d}",
                first_name      = first,
                middle_name     = middle,
                last_name       = last,
                full_name       = full,
                gender          = random.choice(GENDERS),
                date_of_birth   = fake.date_of_birth(minimum_age=17, maximum_age=28),
                category        = random.choice(CATEGORIES),
                admission_type  = random.choice(ADMISSION_TYPES),
                admission_year  = batch,
                batch_year      = batch,
                graduation_year = batch + 4,
                current_semester= random.randint(1, 8),
                current_status  = random.choice(STATUSES),
                email           = f"s{i:06d}@ngiat.edu.in",
                phone           = fake.phone_number()[:15],
                city            = fake.city(),
                state           = random.choice(STATES),
                country         = "India",
            ))

            if len(students) >= BATCH_SIZE:
                db.bulk_save_objects(students)
                db.flush()
                students = []
                print(f"  {i:,} / {TARGET:,} done...")

        if students:
            db.bulk_save_objects(students)
        db.commit()
        print(f"Student seeding complete — {TARGET:,} records.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
