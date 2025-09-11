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
from app.oauth2 import create_access_token


#SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.db_username}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:postgresdefault@localhost:5432/SYS0FAPI_test"


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


@pytest.fixture(scope="function")
def test_user(client):
    user_data = {"email": "jb123@gmail.com",
                 "password": "password123"}
    res = client.post("/users", json=user_data)
    new_user = res.json()
    new_user['password'] = user_data['password']
    assert res.status_code == 201
    return new_user


@pytest.fixture(scope="function")
def test_user2(client):
    user_data = {"email": "sanjeev123@gmail.com",
                 "password": "password123"}
    res = client.post("/users", json=user_data)
    new_user = res.json()
    new_user['password'] = user_data['password']
    assert res.status_code == 201
    return new_user

@pytest.fixture(scope="function")
def token(test_user):
    return create_access_token({"user_id": test_user['user_id']})


@pytest.fixture(scope="function")
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    print(client.headers)
    #yield TestClient(app)
    return client

@pytest.fixture(scope="function")
def test_posts(test_user, session, test_user2):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['user_id']
    }, 
    {
        "title": "second title",
        "content": "second content",
        "owner_id": test_user['user_id']
    },
    {
        "title": "third title",
        "content": "third content",
        "owner_id": test_user['user_id']
    },
    {
        "title": "third title",
        "content": "third content",
        "owner_id": test_user2['user_id']
    }
    ]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    #print("post_map ", post_map)
    posts_list = list(post_map)
    #print("posts list ", posts_list)

    #session.add_all([models.Post(title="asdf", content="asdfj", owner_id=test_user['id']),
    #                 models.Post(title="second title", content="second content", owner_id=test_user['id']),
    #                 models.Post(title="3rd title", content="3rd content", owner_id=test_user['id'])
    #                 ])
    session.add_all(posts_list)
    session.commit()

    posts = session.query(models.Post).order_by(models.Post.id).all()
    return posts