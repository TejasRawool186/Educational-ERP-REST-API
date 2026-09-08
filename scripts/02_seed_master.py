"""
02_seed_master.py
-----------------
Seeds reference / master data for NextGen Institute of AI & Technology (NGIAT).

Exact targets:
  1 institution
  1 campus  (Main Campus only)
  6 departments
  10 programs

Usage:
    python scripts/02_seed_master.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.core.database import SessionLocal
from app.models.institution import Institution
from app.models.campus import Campus
from app.models.department import Department
from app.models.program import Program

INSTITUTION = {
    "institution_code": "NGIAT001",
    "name": "NextGen Institute of AI & Technology",
    "type": "Autonomous Technical Institute",
    "city": "Pune",
    "state": "Maharashtra",
    "country": "India",
    "established_year": 2005,
    "accreditation": "NAAC A+",
    "status": "active",
}

# 1 campus only
CAMPUSES = [
    {
        "campus_code": "NGIAT-MAIN",
        "name": "NextGen Institute of AI & Technology — Main Campus",
        "city": "Pune",
        "state": "Maharashtra",
        "address": "1 NGIAT Road, Hinjewadi, Pune 411057",
        "capacity": 8000,
        "status": "active",
    },
]

# 6 departments
# (name, short_name, established_year)
DEPARTMENTS = [
    ("Computer Science & Engineering",          "CSE",   2005),
    ("Artificial Intelligence & Data Science",  "AIDS",  2010),
    ("Information Technology",                  "IT",    2006),
    ("Electronics & Communication Engineering", "ECE",   2005),
    ("Mechanical Engineering",                  "MECH",  2005),
    ("Basic Sciences & Humanities",             "BSH",   2005),
]

# 10 programs
# (dept_short, code, name, degree_type, duration_years, total_sems, intake)
PROGRAMS = [
    ("CSE",  "BTECH-CSE",   "B.Tech Computer Science & Engineering",        "B.Tech", 4, 8, 120),
    ("CSE",  "MTECH-CE",    "M.Tech Computer Engineering",                  "M.Tech", 2, 4,  30),
    ("AIDS", "BTECH-AIDS",  "B.Tech Artificial Intelligence & Data Science", "B.Tech", 4, 8, 120),
    ("AIDS", "MTECH-AI",    "M.Tech Artificial Intelligence",               "M.Tech", 2, 4,  24),
    ("IT",   "BTECH-IT",    "B.Tech Information Technology",                "B.Tech", 4, 8, 120),
    ("ECE",  "BTECH-ECE",   "B.Tech Electronics & Communication Engineering","B.Tech",4, 8, 120),
    ("ECE",  "MTECH-ECE",   "M.Tech Electronics & Communication",           "M.Tech", 2, 4,  24),
    ("MECH", "BTECH-MECH",  "B.Tech Mechanical Engineering",                "B.Tech", 4, 8,  60),
    ("BSH",  "MSC-MATH",    "M.Sc. Mathematics",                            "M.Sc.",  2, 4,  30),
    ("BSH",  "MSC-PHY",     "M.Sc. Physics",                                "M.Sc.",  2, 4,  20),
]


def seed():
    db = SessionLocal()
    try:
        if db.query(Institution).filter_by(institution_code="NGIAT001").first():
            print("Master data already seeded. Skipping.")
            return

        inst = Institution(**INSTITUTION)
        db.add(inst)
        db.flush()
        print(f"  Institution : {inst.name} (id={inst.id})")

        campus_objs = []
        for c_data in CAMPUSES:
            c = Campus(institution_id=inst.id, **c_data)
            db.add(c)
            campus_objs.append(c)
        db.flush()
        print(f"  Campuses    : {len(campus_objs)}")

        dept_map: dict[str, Department] = {}
        for dept_name, short, est_year in DEPARTMENTS:
            d = Department(
                campus_id=campus_objs[0].id,   # all depts on main campus
                department_code=f"NGIAT-{short}",
                name=dept_name,
                short_name=short,
                established_year=est_year,
                status="active",
            )
            db.add(d)
            dept_map[short] = d
        db.flush()
        print(f"  Departments : {len(dept_map)}")

        prog_count = 0
        for dept_short, code, name, degree, dur, sems, intake in PROGRAMS:
            dept = dept_map[dept_short]
            p = Program(
                department_id=dept.id,
                program_code=code,
                name=name,
                degree_type=degree,
                duration_years=dur,
                total_semesters=sems,
                intake_capacity=intake,
                accreditation_status="NBA Accredited",
                status="active",
            )
            db.add(p)
            prog_count += 1
        db.flush()
        print(f"  Programs    : {prog_count}")

        db.commit()
        print("Master data seeding complete.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
