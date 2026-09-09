from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

database_url= "postgresql://postgres:ajwad321@localhost:5432/nourishpak"
engine= create_engine(database_url)
local_session= sessionmaker(autoflush=False, autocommit= False, bind=engine)
base= declarative_base()

def get_db():
    db= local_session()
    try:
        yield db
    finally:
        db.close()
        