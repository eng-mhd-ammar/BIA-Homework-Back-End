from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from config import DATABASE_URL

Base = declarative_base()
engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)
db_session = SessionLocal()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(150), unique=True, nullable=False)
    password = Column(String(300), nullable=False)

    tables = relationship("UserTables", back_populates="user")


class UserTables(Base):
    __tablename__ = "user_tables"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    table_name = Column(String(255), nullable=False)
    genetic_algorithm_result = Column(JSON, nullable=True, default=[])

    user = relationship("User", back_populates="tables")


# إنشاء الجداول
Base.metadata.create_all(engine)
