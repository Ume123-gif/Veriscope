from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# Transactions
class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, unique=True, index=True)
    account_id = Column(String, index=True)
    transaction_amount = Column(Float)
    transaction_time = Column(DateTime)

# Risk Analyses
class RiskAnalysis(Base):
    __tablename__ = "risk_analyses"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, index=True)
    predicted_class = Column(String)
    xgb_score = Column(Float)
    anomaly_score = Column(Float)
    graph_score = Column(Float)
    risk_score = Column(Float)
    risk_score_percent = Column(Float)
    risk_level = Column(String)
    decision = Column(String)
    community_id = Column(Integer)
    shap_reasons = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

# Audit Logs
class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, index=True)
    action = Column(String)
    decision = Column(String)
    risk_score = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Create Tables
Base.metadata.create_all(bind=engine)