"""
Pydantic schemas for process data validation and serialization.
Defines the structure and validation rules for process-related data.

Author: Cline
"""

from pydantic import BaseModel, EmailStr, constr, validator, Field
from typing import Optional, List
from datetime import datetime
import re
from ..models.database import Department, Frequency, ProcessStatus, VALID_APPS

class ProcessBase(BaseModel):
    """Base Pydantic model for process data."""
    email_id: EmailStr
    department: Department
    process_name: constr(max_length=25)
    description: Optional[constr(max_length=70)] = None
    apps_used: str
    frequency: Frequency
    duration: str
    volume: int = Field(gt=0)
    process_status: ProcessStatus
    documentation: Optional[str] = None

    @validator('duration')
    def validate_duration(cls, v):
        """Validate duration format (HH:MM)."""
        if not re.match(r'^[0-9]{2}:[0-9]{2}$', v):
            raise ValueError('Duration must be in HH:MM format')
        hours, minutes = map(int, v.split(':'))
        if hours > 23 or minutes > 59:
            raise ValueError('Invalid time format')
        return v

    @validator('apps_used')
    def validate_apps(cls, v):
        """Validate apps against predefined list."""
        apps = [app.strip() for app in v.split(',')]
        invalid_apps = [app for app in apps if app not in VALID_APPS]
        if invalid_apps:
            raise ValueError(f'Invalid apps: {", ".join(invalid_apps)}')
        return v

class ProcessCreate(ProcessBase):
    """Schema for creating a new process."""
    pass

class ProcessUpdate(ProcessBase):
    """Schema for updating an existing process."""
    email_id: Optional[EmailStr] = None
    department: Optional[Department] = None
    process_name: Optional[constr(max_length=25)] = None
    apps_used: Optional[str] = None
    frequency: Optional[Frequency] = None
    duration: Optional[str] = None
    volume: Optional[int] = Field(None, gt=0)
    process_status: Optional[ProcessStatus] = None

class ProcessInDB(ProcessBase):
    """Schema for process data as stored in database."""
    id: int
    yearly_volume: int
    yearly_duration: str
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config for ORM mode."""
        from_attributes = True

class ProcessResponse(ProcessInDB):
    """Schema for process response data."""
    pass

class ProcessList(BaseModel):
    """Schema for list of processes."""
    processes: List[ProcessResponse]
    total: int

    class Config:
        """Pydantic config for ORM mode."""
        from_attributes = True
