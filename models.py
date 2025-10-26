from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, JSON, Float
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

    tables = relationship("UserTable", back_populates="user")


class UserTable(Base):
    __tablename__ = "user_tables"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    table_name = Column(String(255), nullable=False)
    source_file = Column(String(255), nullable=True)

    user = relationship("User", back_populates="tables")
    ga_results = relationship("GAResult", back_populates="user_table", cascade="all, delete")
    traditional_results = relationship("TraditionalResult", back_populates="user_table", cascade="all, delete")


class GAResult(Base):
    __tablename__ = "ga_results"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_table_id = Column(Integer, ForeignKey("user_tables.id", ondelete="CASCADE"))
    best_chromosome = Column(JSON, nullable=False)
    selected_features = Column(JSON, nullable=False)
    fitness = Column(Float, nullable=False)

    user_table = relationship("UserTable", back_populates="ga_results")
    generations = relationship("GAGeneration", back_populates="ga_result", cascade="all, delete")


class GAGeneration(Base):
    __tablename__ = "ga_generations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ga_result_id = Column(Integer, ForeignKey("ga_results.id", ondelete="CASCADE"), nullable=False)
    generation = Column(Integer, nullable=False)
    best_genes = Column(JSON, nullable=False)
    avg_fitness = Column(Float, nullable=False)
    best_fitness = Column(Float, nullable=False)

    ga_result = relationship("GAResult", back_populates="generations")
    progressions = relationship("GAProgression", back_populates="generation", cascade="all, delete")  # الربط بالجيل


class GAProgression(Base):
    __tablename__ = "ga_progressions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    generation_id = Column(Integer, ForeignKey("ga_generations.id", ondelete="CASCADE"), nullable=False)
    best_overall_fitness = Column(Float, nullable=False)
    generation_best_fitness = Column(Float, nullable=False)

    generation = relationship("GAGeneration", back_populates="progressions")

class TraditionalResult(Base):
    __tablename__ = "traditional_results"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_table_id = Column(Integer, ForeignKey("user_tables.id", ondelete="CASCADE"))
    
    best_chromosome = Column(JSON, nullable=False)
    selected_features = Column(JSON, nullable=False)
    feature_weights = Column(JSON, nullable=False)
    stages = Column(JSON, nullable=True)
    user_table = relationship("UserTable", back_populates="traditional_results")

from models import UserTable
UserTable.traditional_results = relationship(
    "TraditionalResult", back_populates="user_table", cascade="all, delete"
)


Base.metadata.create_all(engine)