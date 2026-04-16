from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL not found in environment variables. Check your .env file!")

# engine is responsible for managing the connection pool and executing SQL statements
engine = create_engine(DATABASE_URL)

# SessionLocal is a factory for creating new database sessions. It is configured to not autocommit and not autoflush, and it is bound to the engine we created.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
