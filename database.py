from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABSE_URL = "postgresql+psycopg2://bkunbargi:1234@localhost/tododb"

engine = create_engine(SQLALCHEMY_DATABSE_URL)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
session = SessionLocal()
Base = declarative_base()