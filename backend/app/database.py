from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# SQLALCHEMY_DATABASE_URL = 'sqlite://./sql_app.db'
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/devdb"

engine = create_engine(os.environ.get("PG_DATABASE_URL"))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()