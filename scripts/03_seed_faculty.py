"""
03_seed_faculty.py
------------------
Seeds exactly 220 faculty records across 6 departments.

Usage:
    python scripts/03_seed_faculty.py
"""
import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from faker import Faker
from app.core.database import SessionLocal
from app.models.faculty import Faculty
from app.models.department import Department

fake = Faker("en_IN")
random.seed(42)
Faker.seed(42)

TARGET = 220
BATCH_SIZE = 220   # single flush — small enough

DESIGNATIONS = [
    "Professor", "Associate Professor", "Assistant Professor",
    "Senior Lecturer", "Lecturer", "Research Associate",
]
QUALIFICATIONS = ["Ph.D.", "M.Tech + Ph.D.", "M.E.", "M.Tech", "M.Sc", "MBA"]
EMPLOYMENT_TYPES = ["permanent", "permanent", "permanent", "contract", "visiting"]


def seed():
    db = SessionLocal()
    try:
        existing = db.query(Faculty).count()
        if existing >= TARGET:
            print(f"Faculty already seeded ({existing:,}). Skipping.")
            return

        dept_ids = [r[0] for r in db.query(Department.id).all()]
        if not dept_ids:
            print("No departments found. Run 02_seed_master.py first.")
            return

        faculty_list = []
        for i in range(1, TARGET + 1):
            first = fake.first_name()
            last = fake.last_name()
            f = Faculty(
                faculty_uid=f"FAC{i:05d}",
                department_id=random.choice(dept_ids),
                employee_code=f"EMP{i:05d}",
                first_name=first,
                last_name=last,
                full_name=f"{first} {last}",
                designation=random.choice(DESIGNATIONS),
                qualification=random.choice(QUALIFICATIONS),
                specialization=fake.bs(),
                joining_date=fake.date_between(start_date="-20y", end_date="today"),
                experience_years=round(random.uniform(1, 25), 1),
                email=f"faculty{i:05d}@ngiat.edu.in",
                phone=fake.phone_number()[:15],
                employment_type=random.choice(EMPLOYMENT_TYPES),
                status="active",
            )
            faculty_list.append(f)

        db.bulk_save_objects(faculty_list)
        db.commit()
        print(f"Faculty seeding complete — {TARGET} records.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
