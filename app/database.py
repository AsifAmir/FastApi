# psycopg2 adapter for PostgreSQL database connection and SQLAlchemy ORM setup for FastAPI application
import psycopg2
from psycopg2.extras import RealDictCursor
from time import sleep
# SQLAlchemy imports
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# importing the settings from the config module to access environment variables
from app.config import settings

# =======================================================================================================
# Connecting to the database using psycopg2(PostgreSQL driver) for raw SQL queries (not using SQLAlchemy ORM)
# =======================================================================================================
while True:
    try:
        conn = psycopg2.connect(
            host=settings.DB_HOST,
            database=settings.DB_NAME,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        sleep(2)


# =======================================================================================================
# connecting to the database using SQLAlchemy ORM
# =======================================================================================================
# Get the database URL from environment variables
# DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL not found in environment variables. Check your .env file!")

# engine is responsible for managing the connection pool and executing SQL statements
engine = create_engine(DATABASE_URL)

# SessionLocal is a factory for creating new database sessions. It is configured to not autocommit and not autoflush, and it is bound to the engine we created.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base is the base class for our SQLAlchemy models. It is used to define the structure of our database tables and to create the tables in the database.
Base = declarative_base()
# get_db is a dependency function that creates a new database session for each request and ensures that the session is closed after the request is completed. It uses a generator to yield the database session, which allows FastAPI to manage the lifecycle of the session automatically.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
