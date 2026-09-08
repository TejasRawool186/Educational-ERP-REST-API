"""
02_seed_master.py
-----------------
Seeds reference / master data for NextGen Institute of AI & Technology (NGIAT).

Structure:
  1 institution → 2 campuses → 8 departments → programs per department

This script is IDEMPOTENT — running it twice will not create duplicates.
It checks for existing data before inserting.

Version 1 seeds a single institution (institution_id = 1).
The institution table is kept so multi-institution support can be added
in future versions without redesigning the schema.

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

# ── NextGen Institute of AI & Technology (NGIAT) ─────────────────────────────
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

# 2 campuses — main and extended
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
    {
        "campus_code": "NGIAT-EXT",
        "name": "NextGen Institute of AI & Technology — Extended Campus",
        "city": "Pune",
        "state": "Maharashtra",
        "address": "25 Tech Park Avenue, Wakad, Pune 411057",
        "capacity": 4000,
        "status": "active",
    },
]

# 8 departments — all attached to campus 1 (main), except Mechanical/Civil → campus 2
# Each entry: (name, short_name, campus_index[0 or 1], established_year)
DEPARTMENTS = [
    ("Computer Science & Engineering",         "CSE",   0, 2005),
    ("Artificial Intelligence & Data Science", "AIDS",  0, 2010),
    ("Information Technology",                 "IT",    0, 2006),
    ("Electronics & Communication Engineering","ECE",   0, 2005),
    ("Electrical Engineering",                 "EE",    1, 2007),
    ("Mechanical Engineering",                 "MECH",  1, 2005),
    ("Civil Engineering",                      "CIVIL", 1, 2008),
    ("Basic Sciences & Humanities",            "BSH",   0, 2005),
]

# Programs: (dept_short_name, program_code_suffix, name, degree_type, duration_years, total_sems, intake)
PROGRAMS = [
    # CSE
    ("CSE",   "BTECH-CSE",    "B.Tech Computer Science & Engineering",       "B.Tech", 4, 8, 120),
    ("CSE",   "MTECH-CE",     "M.Tech Computer Engineering",                 "M.Tech", 2, 4,  30),
    ("CSE",   "PHD-CSE",      "Ph.D. Computer Science & Engineering",        "Ph.D.",  3, 6,  10),
    # AIDS
    ("AIDS",  "BTECH-AIDS",   "B.Tech Artificial Intelligence & Data Science","B.Tech",4, 8, 120),
    ("AIDS",  "MTECH-AI",     "M.Tech Artificial Intelligence",              "M.Tech", 2, 4,  24),
    # IT
    ("IT",    "BTECH-IT",     "B.Tech Information Technology",               "B.Tech", 4, 8, 120),
    ("IT",    "MTECH-IT",     "M.Tech Information Technology",               "M.Tech", 2, 4,  24),
    # ECE
    ("ECE",   "BTECH-ECE",    "B.Tech Electronics & Communication Engineering","B.Tech",4,8, 120),
    ("ECE",   "MTECH-ECE",    "M.Tech Electronics & Communication",          "M.Tech", 2, 4,  24),
    # EE
    ("EE",    "BTECH-EE",     "B.Tech Electrical Engineering",               "B.Tech", 4, 8,  60),
    # MECH
    ("MECH",  "BTECH-MECH",   "B.Tech Mechanical Engineering",               "B.Tech", 4, 8,  60),
    ("MECH",  "MTECH-MECH",   "M.Tech Mechanical Engineering",               "M.Tech", 2, 4,  18),
    # CIVIL
    ("CIVIL", "BTECH-CIVIL",  "B.Tech Civil Engineering",                    "B.Tech", 4, 8,  60),
    # BSH — service department, no standalone UG program
    ("BSH",   "MSC-MATH",     "M.Sc. Mathematics",                           "M.Sc.",  2, 4,  30),
    ("BSH",   "MSC-PHY",      "M.Sc. Physics",                               "M.Sc.",  2, 4,  20),
]


def seed():
    db = SessionLocal()
    try:
        # ── Idempotency guard ─────────────────────────────────────────────────
        if db.query(Institution).filter_by(institution_code="NGIAT001").first():
            print("Master data already seeded (NGIAT001 exists). Skipping.")
            return

        # ── Institution ───────────────────────────────────────────────────────
        inst = Institution(**INSTITUTION)
        db.add(inst)
        db.flush()   # get inst.id = 1
        print(f"  Institution: {inst.name} (id={inst.id})")

        # ── Campuses ──────────────────────────────────────────────────────────
        campus_objs = []
        for c_data in CAMPUSES:
            c = Campus(institution_id=inst.id, **c_data)
            db.add(c)
            campus_objs.append(c)
        db.flush()
        print(f"  Campuses: {len(campus_objs)}")

        # ── Departments ───────────────────────────────────────────────────────
        dept_map: dict[str, Department] = {}   # short_name → Department
        for dept_name, short, campus_idx, est_year in DEPARTMENTS:
            d = Department(
                campus_id=campus_objs[campus_idx].id,
                department_code=f"NGIAT-{short}",
                name=dept_name,
                short_name=short,
                established_year=est_year,
                status="active",
            )
            db.add(d)
            dept_map[short] = d
        db.flush()
        print(f"  Departments: {len(dept_map)}")

        # ── Programs ─────────────────────────────────────────────────────────
        prog_count = 0
        for dept_short, prog_code, prog_name, degree, dur, sems, intake in PROGRAMS:
            dept = dept_map[dept_short]
            p = Program(
                department_id=dept.id,
                program_code=prog_code,
                name=prog_name,
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
        print(f"  Programs: {prog_count}")

        db.commit()
        print("Master data seeding complete — NextGen Institute of AI & Technology.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
