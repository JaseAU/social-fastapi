from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from app.config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.db_username}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"

# ORM - SQLAlchemy
#engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

class Base(DeclarativeBase):
    pass

def get_db():
    # SessionLocal instance (configured sessionmaker)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
#   with engine.connect() as conn:
#   result = conn.execute(text("select 'hello world'"))
#    print(result.all())


# delay = 2  # seconds to delay retries
# for attempt in range(0, MAX_RETRIES):
#     try:
#         conn = psycopg2.connect(host="localhost",
#                                 database='DEV0FAPI',
#                                 user='postgres',
#                                 password='postgresdefault',
#                                 cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         # print("Database connection was successful")
#         break
#     except Exception as error:
#         if attempt < MAX_RETRIES - 1:
#             print(
#                 f"Error: Attempt {attempt} to connect to DEV0API failed. Trying again..")
#             print("Error: ", error)
#             delay *= 2
#             time.sleep(delay)
#         else:
#             raise