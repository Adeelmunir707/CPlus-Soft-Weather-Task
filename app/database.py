from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote_plus
import json, os

# Load config
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(BASE_DIR, "config.json")) as f:
    db_conf = json.load(f)["database"]

# Encode special characters in password
encoded_password = quote_plus(db_conf["password"])

# Build DB URL
DATABASE_URL = (
    f"postgresql+psycopg2://{db_conf['user']}:{encoded_password}"
    f"@{db_conf['host']}:{db_conf['port']}/{db_conf['dbname']}"
)

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
