from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

database_url="postgresql://postgres:ajwad321@localhost:5432/nourishpak_db"
engine= create_engine(database_url)
session= sessionmaker(autocommit= False, autoflush=False, bind=engine)
base= declarative_base()