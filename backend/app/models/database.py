"""
Database configuration and models for the AutoSwas Process Management System.
Handles SQLAlchemy models and database connection.

Author: Cline
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Enum, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
import enum
from typing import List
import os
from pathlib import Path

# Get the absolute path to the database file
DB_PATH = Path(__file__).parent.parent.parent.parent / "processes.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

# Create SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

# Enum classes for validation
class Department(str, enum.Enum):
    AP = "AP"
    AR = "AR"
    GL = "GL"
    PAYROLL = "Payroll"

class Frequency(str, enum.Enum):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    BI_WEEKLY = "BI_WEEKLY"
    MONTHLY = "MONTHLY"
    QUARTERLY = "QUARTERLY"
    YEARLY = "YEARLY"

    @classmethod
    def get_multiplier(cls, freq: str) -> int:
        """Get the yearly frequency multiplier for a given frequency."""
        multipliers = {
            "DAILY": 220,     # Working days per year
            "WEEKLY": 48,     # Weeks per year (excluding holidays)
            "BI_WEEKLY": 24,  # Bi-weekly occurrences per year
            "MONTHLY": 12,    # Months per year
            "QUARTERLY": 4,   # Quarters per year
            "YEARLY": 1       # Once per year
        }
        return multipliers.get(freq.upper(), 0)

class ProcessStatus(str, enum.Enum):
    """Enum for process status values."""
    UNSTRUCTURED = "UNSTRUCTURED"
    STANDARDIZED = "STANDARDIZED"
    OPTIMIZED = "OPTIMIZED"

# List of valid applications
VALID_APPS = [
    "ERP",
    "Excel",
    "Browser",
    "PDF",
    "Email",
    "Legacy Systems",
    "Reporting Tools"
]

class Process(Base):
    """
    SQLAlchemy model for the processes table.
    Includes all fields with proper constraints and validations.
    """
    __tablename__ = "processes"

    id = Column(Integer, primary_key=True, index=True)
    email_id = Column(String(255), nullable=False)
    department = Column(
        Enum(Department),
        nullable=False
    )
    process_name = Column(
        String(25), 
        nullable=False,
        index=True
    )
    description = Column(
        String(70),
        nullable=True
    )
    apps_used = Column(
        String,
        nullable=False
    )
    frequency = Column(
        Enum(Frequency),
        nullable=False
    )
    duration = Column(
        String,
        CheckConstraint("duration REGEXP '^[0-9]{2}:[0-9]{2}$'"),
        nullable=False
    )
    volume = Column(
        Integer,
        CheckConstraint("volume > 0"),
        nullable=False
    )
    yearly_volume = Column(Integer)
    yearly_duration = Column(String)
    process_status = Column(
        Enum(ProcessStatus),
        nullable=False
    )
    documentation = Column(Text, nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    def __repr__(self):
        """String representation of the Process model."""
        return f"<Process {self.process_name}>"

# Dependency to get database session
def get_db():
    """
    Dependency function to get database session.
    Yields a session and ensures it's closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
