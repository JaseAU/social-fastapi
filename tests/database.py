from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import pytest
from app.config import settings
from app import models
from app.database import get_db, Base
from app.main import app


#SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.db_username}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:postgresdefault@localhost:5432/UAT0FAPI"


# ORM - SQLAlchemy
#engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Override the Database to use a "TEST" database only for pytest.
def override_get_db():
    # SessionLocal instance (configured sessionmaker)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

#client = TestClient(app)

# Create and return a Database session, as well as tear it down and build it up.
@pytest.fixture(scope="function")
def session():
    Base.metadata.drop_all(bind=engine)    # Before our test runs, Use SQL Alchemy to drop tables.
    Base.metadata.create_all(bind=engine)  # Before our test runs, Use SQL Alechemy to build, not Alembic
    #command.upgrade("head")                # Alembic
    #command.downgrade("base")              # Alembic
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create and return a TestClient for testing
@pytest.fixture(scope="function")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)