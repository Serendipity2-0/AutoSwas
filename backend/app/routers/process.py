"""
FastAPI router for process management endpoints.
Handles CRUD operations and file uploads for processes.

Author: Cline
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import logging
from datetime import datetime
import csv
import io

from ..models.database import get_db, Process, Frequency
from ..schemas.process import (
    ProcessCreate,
    ProcessUpdate,
    ProcessResponse,
    ProcessList
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/processes", tags=["processes"])

def calculate_yearly_metrics(process: Process) -> tuple[int, str]:
    """
    Calculate yearly volume and duration for a process.
    
    Args:
        process: Process model instance
        
    Returns:
        tuple: (yearly_volume, yearly_duration)
    """
    try:
        # Calculate yearly volume
        yearly_volume = process.volume * Frequency.get_multiplier(process.frequency.value)
        
        # Calculate yearly duration
        hours, minutes = map(int, process.duration.split(':'))
        total_minutes = (hours * 60 + minutes) * yearly_volume
        
        # Round to nearest 5 minutes
        total_minutes = round(total_minutes / 5) * 5
        
        final_hours = total_minutes // 60
        final_minutes = total_minutes % 60
        
        yearly_duration = f"{final_hours:02d}:{final_minutes:02d}"
        
        return yearly_volume, yearly_duration
    except Exception as e:
        logger.error(f"Error calculating yearly metrics: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error calculating yearly metrics"
        )

@router.post("/", response_model=ProcessResponse)
async def create_process(
    process: ProcessCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new process.
    
    Args:
        process: Process data
        db: Database session
        
    Returns:
        ProcessResponse: Created process
    """
    try:
        db_process = Process(**process.dict())
        
        # Calculate yearly metrics
        yearly_volume, yearly_duration = calculate_yearly_metrics(db_process)
        db_process.yearly_volume = yearly_volume
        db_process.yearly_duration = yearly_duration
        
        db.add(db_process)
        db.commit()
        db.refresh(db_process)
        
        logger.info(f"Created process: {db_process.process_name}")
        return db_process
    except Exception as e:
        logger.error(f"Error creating process: {e}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error creating process: {str(e)}"
        )

@router.get("/", response_model=ProcessList)
async def list_processes(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    department: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    List processes with optional filtering.
    
    Args:
        skip: Number of records to skip
        limit: Number of records to return
        department: Filter by department
        status: Filter by status
        db: Database session
        
    Returns:
        ProcessList: List of processes and total count
    """
    try:
        query = db.query(Process)
        
        # Apply filters
        if department:
            query = query.filter(Process.department == department)
        if status:
            query = query.filter(Process.process_status == status)
            
        total = query.count()
        processes = query.offset(skip).limit(limit).all()
        
        return {
            "processes": processes,
            "total": total
        }
    except Exception as e:
        logger.error(f"Error listing processes: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error listing processes: {str(e)}"
        )

@router.get("/{process_id}", response_model=ProcessResponse)
async def get_process(
    process_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific process by ID.
    
    Args:
        process_id: Process ID
        db: Database session
        
    Returns:
        ProcessResponse: Process details
    """
    process = db.query(Process).filter(Process.id == process_id).first()
    if not process:
        raise HTTPException(status_code=404, detail="Process not found")
    return process

@router.put("/{process_id}", response_model=ProcessResponse)
async def update_process(
    process_id: int,
    process_update: ProcessUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a process.
    
    Args:
        process_id: Process ID
        process_update: Updated process data
        db: Database session
        
    Returns:
        ProcessResponse: Updated process
    """
    try:
        db_process = db.query(Process).filter(Process.id == process_id).first()
        if not db_process:
            raise HTTPException(status_code=404, detail="Process not found")
            
        # Update fields
        update_data = process_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_process, field, value)
            
        # Recalculate yearly metrics if relevant fields changed
        if 'volume' in update_data or 'frequency' in update_data or 'duration' in update_data:
            yearly_volume, yearly_duration = calculate_yearly_metrics(db_process)
            db_process.yearly_volume = yearly_volume
            db_process.yearly_duration = yearly_duration
            
        db.commit()
        db.refresh(db_process)
        
        logger.info(f"Updated process: {db_process.process_name}")
        return db_process
    except Exception as e:
        logger.error(f"Error updating process: {e}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error updating process: {str(e)}"
        )

@router.delete("/{process_id}")
async def delete_process(
    process_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a process.
    
    Args:
        process_id: Process ID
        db: Database session
        
    Returns:
        dict: Success message
    """
    try:
        process = db.query(Process).filter(Process.id == process_id).first()
        if not process:
            raise HTTPException(status_code=404, detail="Process not found")
            
        db.delete(process)
        db.commit()
        
        logger.info(f"Deleted process: {process.process_name}")
        return {"message": "Process deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting process: {e}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting process: {str(e)}"
        )

@router.post("/upload-csv")
async def upload_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload and process a CSV file of processes.
    
    Args:
        file: CSV file
        db: Database session
        
    Returns:
        dict: Success message with import stats
    """
    try:
        if not file.filename.endswith('.csv'):
            raise HTTPException(
                status_code=400,
                detail="Only CSV files are allowed"
            )
            
        content = await file.read()
        csv_data = content.decode('utf-8')
        csv_reader = csv.DictReader(io.StringIO(csv_data))
        
        success_count = 0
        error_count = 0
        errors = []
        
        for row in csv_reader:
            try:
                process_data = ProcessCreate(
                    email_id=row['Email ID'],
                    department=row['Team'],
                    process_name=row['Process Name'],
                    description=row.get('Description', ''),
                    apps_used=row['Apps Used'],
                    frequency=row['Frequency'],
                    duration=row['Duration'],
                    volume=int(row['Volume']),
                    process_status=row['Process Status'],
                    documentation=row.get('Documentation', None)
                )
                
                db_process = Process(**process_data.dict())
                yearly_volume, yearly_duration = calculate_yearly_metrics(db_process)
                db_process.yearly_volume = yearly_volume
                db_process.yearly_duration = yearly_duration
                
                db.add(db_process)
                success_count += 1
                
            except Exception as e:
                error_count += 1
                errors.append(f"Row {csv_reader.line_num}: {str(e)}")
                continue
                
        db.commit()
        
        logger.info(f"CSV import completed: {success_count} successes, {error_count} errors")
        return {
            "message": "CSV import completed",
            "success_count": success_count,
            "error_count": error_count,
            "errors": errors
        }
        
    except Exception as e:
        logger.error(f"Error processing CSV: {e}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error processing CSV: {str(e)}"
        )
