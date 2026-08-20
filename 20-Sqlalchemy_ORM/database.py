from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

database_url = "postgresql://postgres:ajwad321@localhost:5432/nourishpak_db"
engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
base = declarative_base()