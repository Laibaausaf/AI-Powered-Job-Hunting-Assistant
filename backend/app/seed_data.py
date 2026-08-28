"""
Generates >=200 seed job postings (Module A requirement).

Per Section 9's constraint that live scraping may be blocked during judging,
this seeds clearly-labeled synthetic data (source="seed") so the demo works
offline and deterministically. Swap in a real Adzuna/RemoteOK/Jooble fetch
later behind the same Job model without touching the rest of the app -
see the `ingest_from_api()` stub at the bottom for where that goes.

Run with: python -m app.seed_data
"""
import random
import datetime as dt

from app.database import SessionLocal, engine, Base
from app import models

random.seed(42)  # reproducible dataset across runs

ROLE_TEMPLATES = {
    "Frontend Developer": ["React", "JavaScript", "TypeScript", "CSS", "HTML", "Redux"],
    "Backend Developer": ["Python", "Django", "PostgreSQL", "REST APIs", "Docker"],
    "Full Stack Developer": ["React", "Node.js", "MongoDB", "Express", "JavaScript"],
    "Data Analyst": ["SQL", "Python", "Excel", "Tableau", "Power BI"],
    "Data Scientist": ["Python", "Pandas", "Scikit-learn", "SQL", "Statistics"],
    "Machine Learning Engineer": ["Python", "PyTorch", "TensorFlow", "MLOps", "SQL"],
    "DevOps Engineer": ["AWS", "Kubernetes", "Docker", "CI/CD", "Terraform"],
    "Mobile Developer": ["Swift", "Kotlin", "React Native", "Flutter", "REST APIs"],
    "Product Manager": ["Roadmapping", "Agile", "Stakeholder Management", "SQL"],
    "UX Designer": ["Figma", "User Research", "Prototyping", "Wireframing"],
    "QA Engineer": ["Selenium", "Test Automation", "Python", "CI/CD", "Manual Testing"],
    "Cloud Engineer": ["AWS", "Azure", "GCP", "Terraform", "Networking"],
}

LEVELS = ["intern", "entry", "mid", "senior"]
LEVEL_SALARY = {
    "intern": (25000, 40000),
    "entry": (45000, 70000),
    "mid": (75000, 110000),
    "senior": (115000, 170000),
}

COMPANIES = [
    "Northwind Analytics", "Brightpath Labs", "Cascade Systems", "Vertex Digital",
    "Solstice Software", "Harbor Technologies", "Ironclad Cloud", "Lumen Data Co.",
    "Meridian Apps", "Fernwood Tech", "Cobalt Robotics", "Amberline Studios",
    "Granite Fintech", "Willow Health Tech", "Orbit Commerce", "Redshift Analytics",
    "Silverline Networks", "Pinecrest AI", "Bluepeak Software", "Zenith Cloud",
]

LOCATIONS = [
    ("Karachi, Pakistan", "no"), ("Lahore, Pakistan", "no"), ("Islamabad, Pakistan", "no"),
    ("Remote", "yes"), ("Remote (US timezones)", "yes"), ("Remote (EU timezones)", "yes"),
    ("London, UK", "hybrid"), ("Berlin, Germany", "hybrid"), ("New York, USA", "no"),
    ("San Francisco, USA", "hybrid"), ("Toronto, Canada", "hybrid"), ("Singapore", "no"),
]

DESCRIPTION_TEMPLATE = """We are looking for a {level} {title} to join {company}.
You will work with our team on building and scaling products used by thousands of
customers. Required skills: {skills}. This is a {remote_label} position based in
{location}. Salary range: {salary_min}-{salary_max} depending on experience.

Responsibilities:
- Collaborate with cross-functional teams to design and ship features
- Write clean, tested, maintainable code / analysis
- Participate in code reviews and technical planning
- Continuously improve our tools and processes using {primary_skill}

Nice to have: familiarity with agile workflows and a strong communicator."""


def build_jobs(n=250):
    jobs = []
    today = dt.datetime.utcnow()
    for i in range(n):
        title = random.choice(list(ROLE_TEMPLATES.keys()))
        skills = ROLE_TEMPLATES[title]
        level = random.choice(LEVELS)
        company = random.choice(COMPANIES)
        location, remote = random.choice(LOCATIONS)
        salary_min, salary_max = LEVEL_SALARY[level]
        # add some noise to salary so ranges aren't identical across postings
        salary_min = int(salary_min * random.uniform(0.9, 1.05))
        salary_max = int(salary_max * random.uniform(0.95, 1.15))
        posted_days_ago = random.randint(0, 75)  # spread over ~2.5 months
        remote_label = {"yes": "fully remote", "no": "on-site", "hybrid": "hybrid"}[remote]

        description = DESCRIPTION_TEMPLATE.format(
            level=level, title=title, company=company,
            skills=", ".join(skills), remote_label=remote_label,
            location=location, salary_min=salary_min, salary_max=salary_max,
            primary_skill=skills[0],
        )

        jobs.append(models.Job(
            title=f"{level.capitalize()} {title}" if level != "mid" else title,
            company=company,
            location=location,
            remote=remote,
            role_level=level,
            salary_min=salary_min,
            salary_max=salary_max,
            description=description,
            skills=skills,
            posted_date=today - dt.timedelta(days=posted_days_ago),
            source="seed",
        ))
    return jobs


def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        existing = db.query(models.Job).count()
        if existing >= 200:
            print(f"Jobs table already has {existing} rows, skipping seed.")
            return
        jobs = build_jobs(250)
        db.add_all(jobs)
        db.commit()
        print(f"Seeded {len(jobs)} jobs.")
    finally:
        db.close()


def ingest_from_api():
    """
    Stub for the 6.2 bonus: live integration with a public job API
    (Adzuna, RemoteOK, Jooble). Fetch postings, map fields onto the same
    Job model used here, set source="<api_name>" instead of "seed", and
    insert with the same db.add_all() pattern as run(). Left unimplemented
    so the MVP works without any external API key.
    """
    raise NotImplementedError("Wire up a real job API here for the bonus points.")


if __name__ == "__main__":
    run()
