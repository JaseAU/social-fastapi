from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Post(Base):

    __tablename__ = "posts"
    __table_args__ = {"schema": "fapisysdb"}

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    published: Mapped[bool] = mapped_column(
        server_default="TRUE", nullable=False)
    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id: Mapped[int] = mapped_column(ForeignKey("fapisysdb.users.user_id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User")
    # id = Column(Integer, primary_key=True, nullable=False)
    # title = Column(String, nullable=False)
    # content = Column(String, nullable=False)
    # published = Column(Boolean, default=True)
    # created_by = Column()
    # __table_args__=


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "fapisysdb"}

    user_id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    phone_number: Mapped[str] = mapped_column(nullable=True)

class Vote(Base):
    __tablename__ = "votes"
    __table_args__ = {"schema": "fapisysdb"}

    post_id: Mapped[int] = mapped_column(ForeignKey("fapisysdb.posts.id", ondelete="CASCADE"), 
                                         primary_key=True,nullable=False)
    voter_id: Mapped[int] = mapped_column(ForeignKey("fapisysdb.users.user_id", ondelete="CASCADE"), 
                                          primary_key=True, nullable=False)

    

    