import os
from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey, Enum as SAEnum,
    JSON, Float, Boolean, create_engine, Index
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import enum
from datetime import datetime

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///fairfin.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

Base = declarative_base()

# ---------------------------
# Enums
# ---------------------------
class LoanStatus(enum.Enum):
    pending = "pending"
    approved = "approved"
    denied = "denied"
    withdrawn = "withdrawn"


# ---------------------------
# User Table
# ---------------------------
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    auth0_id = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(120), nullable=True)

    # Email should not be nullable because the system relies on it as a primary identity key
    email = Column(String(255), unique=True, index=True, nullable=False)
    
    # Default stored value avoids empty DB state
    role = Column(String(20), nullable=False, default="pending")  # pending → choose role on first login

    loans = relationship("LoanApplication", back_populates="user", cascade="all, delete-orphan")
    auditlogs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")
    edit_requests = relationship("EditRequest", back_populates="user", cascade="all, delete-orphan")


# ---------------------------
# Loan Table
# ---------------------------
class LoanApplication(Base):
    __tablename__ = "loan_applications"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Store request payload
    application_data = Column(JSON, nullable=False)

    decision = Column(String(20), nullable=True)

    status = Column(
        SAEnum(LoanStatus),
        default=LoanStatus.pending,
        nullable=False
    )

    explanation = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="loans")
    edit_requests = relationship("EditRequest", back_populates="loan", cascade="all, delete-orphan")


# Add index so analysts/admins can quickly fetch pending items
Index("idx_loan_status", LoanApplication.status)


# ---------------------------
# Logs
# ---------------------------
class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String(500), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="auditlogs")


# ---------------------------
# Edit Request Table
# ---------------------------
class EditRequest(Base):
    __tablename__ = "edit_requests"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    loan_application_id = Column(Integer, ForeignKey("loan_applications.id"), nullable=False)

    new_monthly_expenses = Column(Float, nullable=True)
    new_existing_loans = Column(Integer, nullable=True)
    new_loan_tenure = Column(Integer, nullable=True)
    
    withdraw_requested = Column(Boolean, default=False, nullable=False)
    
    status = Column(String(20), default="pending", nullable=False)  # pending|approved|rejected
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="edit_requests")
    loan = relationship("LoanApplication", back_populates="edit_requests")


# ---------------------------
# Init DB
# ---------------------------
def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("Database initialized.")
