"""
07_seed_career.py
-----------------
Seeds career and activity data to hit these EXACT targets:

  Internships              1,800
  Placements               1,500
  Higher Studies             500
  Entrepreneurship           150
  Projects                 3,500
  Certifications           2,500
  Publications               400
  Professional Activities  5,000
  Awards                     650
  Backlogs                 4,000  (spread across academic_performance — set in 06)

Usage:
    python scripts/07_seed_career.py
"""
import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from faker import Faker
from app.core.database import SessionLocal
from app.models.student import Student
from app.models.placement import Placement
from app.models.internship import Internship
from app.models.higher_studies import HigherStudies
from app.models.entrepreneurship import Entrepreneurship
from app.models.project import Project
from app.models.certification import Certification
from app.models.publication import Publication
from app.models.professional_activity import ProfessionalActivity
from app.models.award import Award

fake = Faker("en_IN")
random.seed(42)
Faker.seed(42)

# ── Reference data ────────────────────────────────────────────────────────────
COMPANIES   = ["TCS", "Infosys", "Wipro", "HCL", "Cognizant", "Accenture", "IBM",
               "Google", "Microsoft", "Amazon", "Flipkart", "Zomato", "HDFC",
               "Deloitte", "Capgemini", "L&T Infotech", "Mphasis", "Tech Mahindra"]
INDUSTRIES  = ["IT Services", "Product", "BFSI", "Consulting", "E-Commerce", "Manufacturing"]
ROLES       = ["Software Engineer", "Data Analyst", "DevOps Engineer", "Business Analyst",
               "Cloud Engineer", "ML Engineer", "Systems Engineer", "QA Engineer"]
PKG_BANDS   = [(3,5),(5,8),(8,12),(12,20),(20,40)]
PKG_WEIGHTS = [30, 35, 20, 10, 5]
HS_COUNTRIES= ["India","USA","Canada","Germany","UK","Australia","Singapore"]
HS_DEGREES  = ["M.Tech","MS","MBA","MCA","Ph.D.","Other"]
DOMAINS     = ["AI/ML","Web Dev","Mobile","Data Science","Networking","Security","Cloud","IoT"]
STARTUP_IND = ["AI","FinTech","EdTech","HealthTech","SaaS","Agritech","E-commerce"]
ACT_TYPES   = ["Hackathon","Workshop","Seminar","Conference","Technical Event","Sports","Cultural"]
CERT_ORGS   = ["Coursera","NPTEL","AWS","Google","Microsoft","Oracle","Red Hat","Udemy"]
CERT_DOMS   = ["Cloud","AI","Cybersecurity","Data Science","DevOps","Web Dev","Database"]
AWD_LEVELS  = ["Institute","State","National","International"]
AWD_CATS    = ["Academic Excellence","Sports","Cultural","Research","Innovation"]
TECH_STACK  = ["Python","React","Node.js","Java","Go","TensorFlow","AWS","Docker",
               "Kubernetes","Flutter","Django","Spring Boot","PostgreSQL","MongoDB"]

BATCH = 300

def _pkg():
    band = random.choices(PKG_BANDS, weights=PKG_WEIGHTS, k=1)[0]
    return round(random.uniform(*band), 2)

def bulk(db, batch):
    if batch:
        db.bulk_save_objects(batch)
        db.flush()

def seed():
    db = SessionLocal()
    try:
        student_ids = [r[0] for r in db.query(Student.id).all()]
        if not student_ids:
            print("No students found. Run earlier scripts first.")
            return

        total = len(student_ids)
        print(f"Seeding career data for {total:,} students...")

        # ── Placements — exactly 1,500 ────────────────────────────────────────
        if db.query(Placement).count() == 0:
            target = min(1500, total)
            chosen = random.sample(student_ids, k=target)
            batch = []
            for sid in chosen:
                batch.append(Placement(
                    student_id=sid,
                    company_name=random.choice(COMPANIES),
                    company_type=random.choice(["MNC","Startup","PSU"]),
                    industry=random.choice(INDUSTRIES),
                    placement_type=random.choice(["Campus","Off-Campus","PPO"]),
                    job_role=random.choice(ROLES),
                    package_lpa=_pkg(),
                    placement_date=fake.date_between(start_date="-3y", end_date="today"),
                    offer_status="accepted",
                    joining_status="joined",
                    location=fake.city(),
                ))
                if len(batch) >= BATCH: bulk(db, batch); batch = []
            bulk(db, batch)
            print(f"  Placements              : {db.query(Placement).count():,}")

        # ── Internships — exactly 1,800 ───────────────────────────────────────
        if db.query(Internship).count() == 0:
            target = min(1800, total)
            chosen = random.sample(student_ids, k=target)
            batch = []
            for sid in chosen:
                batch.append(Internship(
                    student_id=sid,
                    company_name=random.choice(COMPANIES),
                    internship_type=random.choice(["industry","research","virtual"]),
                    start_date=fake.date_between(start_date="-3y", end_date="-3m"),
                    end_date=fake.date_between(start_date="-3m", end_date="today"),
                    duration_days=random.randint(30, 180),
                    domain=random.choice(DOMAINS),
                    role=random.choice(ROLES),
                    stipend=random.choice([0, 5000, 10000, 15000, 20000]),
                    location=fake.city(),
                    completion_status="completed",
                    certificate_available=random.random() > 0.25,
                ))
                if len(batch) >= BATCH: bulk(db, batch); batch = []
            bulk(db, batch)
            print(f"  Internships             : {db.query(Internship).count():,}")

        # ── Higher Studies — exactly 500 ──────────────────────────────────────
        if db.query(HigherStudies).count() == 0:
            target = min(500, total)
            chosen = random.sample(student_ids, k=target)
            batch = []
            for sid in chosen:
                batch.append(HigherStudies(
                    student_id=sid,
                    institution_name=fake.company() + " University",
                    country=random.choice(HS_COUNTRIES),
                    program=f"M.Tech {random.choice(DOMAINS)}",
                    degree_type=random.choice(HS_DEGREES),
                    specialization=random.choice(DOMAINS),
                    admission_year=random.randint(2021, 2025),
                    scholarship=random.choice([None,"Merit","Government","University"]),
                    status=random.choice(["pursuing","completed"]),
                ))
                if len(batch) >= BATCH: bulk(db, batch); batch = []
            bulk(db, batch)
            print(f"  Higher Studies          : {db.query(HigherStudies).count():,}")

        # ── Entrepreneurship — exactly 150 ────────────────────────────────────
        if db.query(Entrepreneurship).count() == 0:
            target = min(150, total)
            chosen = random.sample(student_ids, k=target)
            batch = []
            for sid in chosen:
                batch.append(Entrepreneurship(
                    student_id=sid,
                    startup_name=fake.company(),
                    startup_type=random.choice(["Bootstrapped","Funded","Stealth"]),
                    industry=random.choice(STARTUP_IND),
                    founding_year=random.randint(2019, 2025),
                    role=random.choice(["Founder","Co-Founder","CTO","CEO"]),
                    funding_stage=random.choice(["Pre-seed","Seed","Bootstrapped"]),
                    funding_amount=random.choice([None, 500000, 1000000]),
                    employees=random.randint(1, 30),
                    status=random.choice(["active","active","closed"]),
                ))
                if len(batch) >= BATCH: bulk(db, batch); batch = []
            bulk(db, batch)
            print(f"  Entrepreneurship        : {db.query(Entrepreneurship).count():,}")

        # ── Projects — exactly 3,500 ──────────────────────────────────────────
        if db.query(Project).count() == 0:
            # distribute ~3,500 projects across all students
            # ~0.875 projects per student on average, some get 1 some get 0
            project_student_ids = random.choices(student_ids, k=3500)
            batch = []
            for i, sid in enumerate(project_student_ids, 1):
                batch.append(Project(
                    student_id=sid,
                    project_title=f"{random.choice(DOMAINS)} — Project {i:04d}",
                    project_type=random.choice(["major","minor","research"]),
                    domain=random.choice(DOMAINS),
                    description=fake.sentence(nb_words=12),
                    start_date=fake.date_between(start_date="-3y", end_date="-4m"),
                    end_date=fake.date_between(start_date="-4m", end_date="today"),
                    technology_stack=", ".join(random.sample(TECH_STACK, k=3)),
                    status="completed",
                ))
                if len(batch) >= BATCH: bulk(db, batch); batch = []
            bulk(db, batch)
            print(f"  Projects                : {db.query(Project).count():,}")

        # ── Certifications — exactly 2,500 ───────────────────────────────────
        if db.query(Certification).count() == 0:
            cert_ids = random.choices(student_ids, k=2500)
            batch = []
            for sid in cert_ids:
                batch.append(Certification(
                    student_id=sid,
                    certification_name=f"{random.choice(CERT_DOMS)} Certification",
                    issuing_organization=random.choice(CERT_ORGS),
                    issue_date=fake.date_between(start_date="-3y", end_date="today"),
                    domain=random.choice(CERT_DOMS),
                    status="active",
                ))
                if len(batch) >= BATCH: bulk(db, batch); batch = []
            bulk(db, batch)
            print(f"  Certifications          : {db.query(Certification).count():,}")

        # ── Publications — exactly 400 ────────────────────────────────────────
        if db.query(Publication).count() == 0:
            pub_ids = random.choices(student_ids, k=400)
            batch = []
            for sid in pub_ids:
                batch.append(Publication(
                    student_id=sid,
                    title=fake.sentence(nb_words=9),
                    publication_type=random.choice(["journal","conference","book_chapter"]),
                    journal_name=fake.company() + " Journal",
                    publication_date=fake.date_between(start_date="-3y", end_date="today"),
                    indexed=random.random() > 0.45,
                    indexing_database=random.choice(["Scopus","SCI","IEEE","Springer",None]),
                    status="published",
                ))
                if len(batch) >= BATCH: bulk(db, batch); batch = []
            bulk(db, batch)
            print(f"  Publications            : {db.query(Publication).count():,}")

        # ── Professional Activities — exactly 5,000 ───────────────────────────
        if db.query(ProfessionalActivity).count() == 0:
            act_ids = random.choices(student_ids, k=5000)
            batch = []
            for sid in act_ids:
                batch.append(ProfessionalActivity(
                    student_id=sid,
                    activity_type=random.choice(ACT_TYPES),
                    title=fake.sentence(nb_words=6),
                    organization=fake.company(),
                    activity_date=fake.date_between(start_date="-3y", end_date="today"),
                    role=random.choice(["Participant","Organizer","Winner","Speaker"]),
                    outcome=random.choice(["Winner","Runner-Up","Participant","Qualified"]),
                    certificate_available=random.random() > 0.35,
                ))
                if len(batch) >= BATCH: bulk(db, batch); batch = []
            bulk(db, batch)
            print(f"  Professional Activities : {db.query(ProfessionalActivity).count():,}")

        # ── Awards — exactly 650 ──────────────────────────────────────────────
        if db.query(Award).count() == 0:
            awd_ids = random.choices(student_ids, k=650)
            batch = []
            for sid in awd_ids:
                batch.append(Award(
                    student_id=sid,
                    award_name=f"{random.choice(AWD_CATS)} Award",
                    award_category=random.choice(AWD_CATS),
                    awarding_body=fake.company(),
                    award_date=fake.date_between(start_date="-3y", end_date="today"),
                    level=random.choice(AWD_LEVELS),
                    position=random.choice(["1st","2nd","3rd","Participant"]),
                    description=fake.sentence(),
                ))
                if len(batch) >= BATCH: bulk(db, batch); batch = []
            bulk(db, batch)
            print(f"  Awards                  : {db.query(Award).count():,}")

        db.commit()
        print("\nCareer seeding complete.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
