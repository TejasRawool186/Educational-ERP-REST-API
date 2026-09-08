"""
07_seed_career.py
-----------------
Seeds career-outcome data:
  placements, internships, higher studies, entrepreneurship,
  projects, certifications, publications, professional activities, awards.

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

COMPANIES = ["TCS", "Infosys", "Wipro", "HCL", "Cognizant", "Accenture", "IBM",
             "Google", "Microsoft", "Amazon", "Flipkart", "Zomato", "HDFC", "Deloitte"]
INDUSTRIES = ["IT Services", "Product", "BFSI", "Consulting", "E-Commerce", "Manufacturing"]
ROLES = ["Software Engineer", "Data Analyst", "DevOps Engineer", "Business Analyst",
         "Cloud Engineer", "ML Engineer", "Systems Engineer"]
PACKAGE_BANDS = [(3, 5), (5, 8), (8, 12), (12, 20), (20, 40), (40, 80)]
BAND_WEIGHTS = [25, 35, 20, 10, 7, 3]

HS_COUNTRIES = ["India", "USA", "Canada", "Germany", "UK", "Australia", "Singapore"]
HS_DEGREES = ["M.Tech", "MS", "MBA", "MCA", "Ph.D.", "Other"]
STARTUP_TYPES = ["Bootstrapped", "Funded", "Stealth"]
INDUSTRIES_E = ["AI", "FinTech", "EdTech", "HealthTech", "SaaS", "Cybersecurity", "Agritech", "E-commerce"]
DOMAINS = ["AI/ML", "Web Dev", "Mobile", "Data Science", "Networking", "Security", "Cloud", "IoT"]
ACTIVITY_TYPES = ["Hackathon", "Workshop", "Seminar", "Conference", "Technical Event", "Sports", "Cultural"]
CERT_ORGS = ["Coursera", "Udemy", "NPTEL", "AWS", "Google", "Microsoft", "Oracle", "Red Hat"]
CERT_DOMAINS = ["Cloud", "AI", "Cybersecurity", "Data Science", "DevOps", "Web Dev", "Database"]
AWARD_LEVELS = ["Institute", "State", "National", "International"]
AWARD_CATEGORIES = ["Academic Excellence", "Sports", "Cultural", "Research", "Innovation"]

BATCH = 500


def _pkg():
    band = random.choices(PACKAGE_BANDS, weights=BAND_WEIGHTS, k=1)[0]
    return round(random.uniform(*band), 2)


def seed():
    db = SessionLocal()
    try:
        student_ids = [r[0] for r in db.query(Student.id).all()]
        if not student_ids:
            print("No students found. Run earlier scripts first.")
            return

        total = len(student_ids)
        print(f"Seeding career data for {total:,} students...")

        # ── Placements (~30%) ─────────────────────────────────────────────────
        if db.query(Placement).count() == 0:
            placed = random.sample(student_ids, k=int(total * 0.30))
            batch = []
            for sid in placed:
                company = random.choice(COMPANIES)
                batch.append(Placement(
                    student_id=sid, company_name=company,
                    company_type="MNC" if random.random() > 0.4 else "Startup",
                    industry=random.choice(INDUSTRIES),
                    placement_type=random.choice(["Campus", "Off-Campus", "PPO"]),
                    job_role=random.choice(ROLES),
                    package_lpa=_pkg(),
                    placement_date=fake.date_between(start_date="-3y", end_date="today"),
                    offer_status="accepted",
                    joining_status="joined",
                    location=fake.city(),
                ))
                if len(batch) >= BATCH:
                    db.bulk_save_objects(batch); batch = []
            if batch: db.bulk_save_objects(batch)
            db.flush(); print(f"  Placements: {len(placed):,}")

        # ── Internships (~50%) ────────────────────────────────────────────────
        if db.query(Internship).count() == 0:
            intern_studs = random.sample(student_ids, k=int(total * 0.50))
            batch = []
            for sid in intern_studs:
                batch.append(Internship(
                    student_id=sid,
                    company_name=random.choice(COMPANIES),
                    internship_type=random.choice(["industry", "research", "virtual"]),
                    start_date=fake.date_between(start_date="-4y", end_date="-1y"),
                    end_date=fake.date_between(start_date="-1y", end_date="today"),
                    duration_days=random.randint(30, 180),
                    domain=random.choice(DOMAINS),
                    role=random.choice(ROLES),
                    stipend=random.choice([0, 5000, 10000, 15000, 20000]),
                    location=fake.city(),
                    completion_status="completed",
                    certificate_available=random.random() > 0.2,
                ))
                if len(batch) >= BATCH:
                    db.bulk_save_objects(batch); batch = []
            if batch: db.bulk_save_objects(batch)
            db.flush(); print(f"  Internships: {len(intern_studs):,}")

        # ── Higher Studies (~15%) ─────────────────────────────────────────────
        if db.query(HigherStudies).count() == 0:
            hs_studs = random.sample(student_ids, k=int(total * 0.15))
            batch = []
            for sid in hs_studs:
                batch.append(HigherStudies(
                    student_id=sid,
                    institution_name=fake.company() + " University",
                    country=random.choice(HS_COUNTRIES),
                    program=f"M.Tech {random.choice(DOMAINS)}",
                    degree_type=random.choice(HS_DEGREES),
                    specialization=random.choice(DOMAINS),
                    admission_year=random.randint(2021, 2025),
                    scholarship=random.choice([None, "Merit", "Government", "University"]),
                    status="pursuing",
                ))
                if len(batch) >= BATCH:
                    db.bulk_save_objects(batch); batch = []
            if batch: db.bulk_save_objects(batch)
            db.flush(); print(f"  Higher Studies: {len(hs_studs):,}")

        # ── Entrepreneurship (~5%) ────────────────────────────────────────────
        if db.query(Entrepreneurship).count() == 0:
            entr_studs = random.sample(student_ids, k=int(total * 0.05))
            batch = []
            for sid in entr_studs:
                batch.append(Entrepreneurship(
                    student_id=sid,
                    startup_name=fake.company(),
                    startup_type=random.choice(STARTUP_TYPES),
                    industry=random.choice(INDUSTRIES_E),
                    founding_year=random.randint(2018, 2025),
                    role=random.choice(["Founder", "Co-Founder", "CTO", "CEO"]),
                    funding_stage=random.choice(["Pre-seed", "Seed", "Series A", "Bootstrapped"]),
                    funding_amount=random.choice([None, 500000, 1000000, 5000000]),
                    employees=random.randint(1, 50),
                    status=random.choice(["active", "active", "closed"]),
                ))
                if len(batch) >= BATCH:
                    db.bulk_save_objects(batch); batch = []
            if batch: db.bulk_save_objects(batch)
            db.flush(); print(f"  Entrepreneurship: {len(entr_studs):,}")

        # ── Projects (~100% × 1 each) ─────────────────────────────────────────
        if db.query(Project).count() == 0:
            batch = []
            for i, sid in enumerate(student_ids, 1):
                n = random.randint(1, 3)
                for _ in range(n):
                    batch.append(Project(
                        student_id=sid,
                        project_title=f"{random.choice(DOMAINS)} Project by STU{sid}",
                        project_type=random.choice(["major", "minor", "research"]),
                        domain=random.choice(DOMAINS),
                        description=fake.sentence(),
                        start_date=fake.date_between(start_date="-3y", end_date="-6m"),
                        end_date=fake.date_between(start_date="-6m", end_date="today"),
                        technology_stack=", ".join(random.sample(
                            ["Python", "React", "Node.js", "Java", "Go", "TensorFlow", "AWS", "Docker"], k=3
                        )),
                        status="completed",
                    ))
                if len(batch) >= BATCH:
                    db.bulk_save_objects(batch); batch = []
            if batch: db.bulk_save_objects(batch)
            db.flush(); print(f"  Projects seeded")

        # ── Certifications (~75%) ─────────────────────────────────────────────
        if db.query(Certification).count() == 0:
            cert_studs = random.sample(student_ids, k=int(total * 0.75))
            batch = []
            for sid in cert_studs:
                n = random.randint(1, 3)
                for _ in range(n):
                    batch.append(Certification(
                        student_id=sid,
                        certification_name=f"{random.choice(CERT_DOMAINS)} Certification",
                        issuing_organization=random.choice(CERT_ORGS),
                        issue_date=fake.date_between(start_date="-3y", end_date="today"),
                        domain=random.choice(CERT_DOMAINS),
                        status="active",
                    ))
                if len(batch) >= BATCH:
                    db.bulk_save_objects(batch); batch = []
            if batch: db.bulk_save_objects(batch)
            db.flush(); print(f"  Certifications seeded")

        # ── Publications (~20%) ───────────────────────────────────────────────
        if db.query(Publication).count() == 0:
            pub_studs = random.sample(student_ids, k=int(total * 0.20))
            batch = []
            for sid in pub_studs:
                batch.append(Publication(
                    student_id=sid,
                    title=fake.sentence(nb_words=8),
                    publication_type=random.choice(["journal", "conference", "book_chapter"]),
                    journal_name=fake.company() + " Journal",
                    publication_date=fake.date_between(start_date="-3y", end_date="today"),
                    indexed=random.random() > 0.4,
                    indexing_database=random.choice(["Scopus", "SCI", "IEEE", "Springer", None]),
                    status="published",
                ))
                if len(batch) >= BATCH:
                    db.bulk_save_objects(batch); batch = []
            if batch: db.bulk_save_objects(batch)
            db.flush(); print(f"  Publications: {len(pub_studs):,}")

        # ── Professional Activities (~100%) ───────────────────────────────────
        if db.query(ProfessionalActivity).count() == 0:
            batch = []
            for sid in student_ids:
                n = random.randint(1, 4)
                for _ in range(n):
                    batch.append(ProfessionalActivity(
                        student_id=sid,
                        activity_type=random.choice(ACTIVITY_TYPES),
                        title=fake.sentence(nb_words=5),
                        organization=fake.company(),
                        activity_date=fake.date_between(start_date="-3y", end_date="today"),
                        role=random.choice(["Participant", "Organizer", "Winner", "Speaker"]),
                        outcome=random.choice(["Winner", "Runner-Up", "Participant", "Qualified"]),
                        certificate_available=random.random() > 0.3,
                    ))
                if len(batch) >= BATCH:
                    db.bulk_save_objects(batch); batch = []
            if batch: db.bulk_save_objects(batch)
            db.flush(); print(f"  Professional Activities seeded")

        # ── Awards (~15%) ─────────────────────────────────────────────────────
        if db.query(Award).count() == 0:
            award_studs = random.sample(student_ids, k=int(total * 0.15))
            batch = []
            for sid in award_studs:
                batch.append(Award(
                    student_id=sid,
                    award_name=f"{random.choice(AWARD_CATEGORIES)} Award",
                    award_category=random.choice(AWARD_CATEGORIES),
                    awarding_body=fake.company(),
                    award_date=fake.date_between(start_date="-3y", end_date="today"),
                    level=random.choice(AWARD_LEVELS),
                    position=random.choice(["1st", "2nd", "3rd", "Participant"]),
                    description=fake.sentence(),
                ))
                if len(batch) >= BATCH:
                    db.bulk_save_objects(batch); batch = []
            if batch: db.bulk_save_objects(batch)
            db.flush(); print(f"  Awards: {len(award_studs):,}")

        db.commit()
        print("Career data seeding complete.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
