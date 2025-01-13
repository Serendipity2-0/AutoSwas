#!/usr/bin/env python3
"""
Database initialization script for AutoSwas Process Management System.
Creates SQLite database with proper schema and imports sample data.

Author: Cline
"""

import pandas as pd
import sqlite3
from datetime import datetime
import re
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants for ENUM values and calculations
DEPARTMENTS = ['AP', 'AR', 'GL', 'Payroll']
APPS = ['ERP', 'Excel', 'Browser', 'PDF', 'Email', 'Legacy Systems', 'Reporting Tools']
FREQUENCIES = ['DAILY', 'WEEKLY', 'BI_WEEKLY', 'MONTHLY', 'QUARTERLY', 'YEARLY']
PROCESS_STATUSES = ['UNSTRUCTURED', 'STANDARDIZED', 'OPTIMIZED']

# Frequency mapping for data import
FREQUENCY_MAPPING = {
    'Daily': 'DAILY',
    'Weekly': 'WEEKLY',
    'Bi-Weekly': 'BI_WEEKLY',
    'Monthly': 'MONTHLY',
    'Quarterly': 'QUARTERLY',
    'Yearly': 'YEARLY'
}

# Yearly frequency multipliers
FREQUENCY_MULTIPLIERS = {
    'DAILY': 220,      # Working days per year
    'WEEKLY': 48,      # Weeks per year (excluding holidays)
    'BI_WEEKLY': 24,   # Bi-weekly occurrences per year
    'MONTHLY': 12,     # Months per year
    'QUARTERLY': 4,    # Quarters per year
    'YEARLY': 1        # Once per year
}

def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_time_format(time_str: str) -> bool:
    """Validate time format (HH:MM)."""
    try:
        datetime.strptime(time_str, '%H:%M')
        return True
    except ValueError:
        return False

def calculate_yearly_volume(volume: int, frequency: str) -> int:
    """Calculate yearly volume based on frequency multiplier."""
    return volume * FREQUENCY_MULTIPLIERS.get(frequency, 0)

def calculate_yearly_duration(duration: str, yearly_volume: int) -> str:
    """
    Calculate yearly duration in HH:MM format.
    Rounds minutes to nearest 5 minutes.
    """
    try:
        hours, minutes = map(int, duration.split(':'))
        total_minutes = (hours * 60 + minutes) * yearly_volume
        
        # Round to nearest 5 minutes
        total_minutes = round(total_minutes / 5) * 5
        
        final_hours = total_minutes // 60
        final_minutes = total_minutes % 60
        
        return f"{final_hours:02d}:{final_minutes:02d}"
    except ValueError as e:
        logger.error(f"Error calculating yearly duration: {e}")
        return "00:00"

def create_database():
    """Create SQLite database with proper schema."""
    try:
        conn = sqlite3.connect('processes.db')
        cursor = conn.cursor()
        
        # Create processes table with proper schema
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS processes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email_id TEXT NOT NULL CHECK (length(email_id) <= 255),
            department TEXT NOT NULL CHECK (department IN ({})),
            process_name TEXT NOT NULL CHECK (length(process_name) <= 25),
            description TEXT CHECK (length(description) <= 70),
            apps_used TEXT NOT NULL,
            frequency TEXT NOT NULL CHECK (frequency IN ({})),
            duration TEXT NOT NULL,
            volume INTEGER NOT NULL CHECK (volume > 0),
            yearly_volume INTEGER,
            yearly_duration TEXT,
            process_status TEXT NOT NULL CHECK (process_status IN ({})),
            documentation TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        '''.format(
            ','.join(f"'{dept}'" for dept in DEPARTMENTS),
            ','.join(f"'{freq}'" for freq in FREQUENCIES),
            ','.join(f"'{status}'" for status in PROCESS_STATUSES)
        ))
        
        # Create trigger to update timestamp
        cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS update_timestamp 
        AFTER UPDATE ON processes
        BEGIN
            UPDATE processes SET updated_at = CURRENT_TIMESTAMP 
            WHERE id = NEW.id;
        END;
        ''')
        
        conn.commit()
        logger.info("Database schema created successfully")
        return conn
    except sqlite3.Error as e:
        logger.error(f"Error creating database: {e}")
        raise

def import_sample_data(conn: sqlite3.Connection):
    """Import and validate sample data from CSV."""
    try:
        df = pd.read_csv('SampleData.csv')
        
        # Data validation and transformation
        valid_records = []
        for _, row in df.iterrows():
            # Skip if required fields are missing
            if pd.isna(row['Email ID']) or pd.isna(row['Team']) or pd.isna(row['Process Name']):
                logger.warning(f"Skipping row with missing required fields: {row['Process Name']}")
                continue
                
            # Validate email
            if not validate_email(row['Email ID']):
                logger.warning(f"Invalid email format: {row['Email ID']}")
                continue
                
            # Validate duration format
            if not validate_time_format(row['Duration']):
                logger.warning(f"Invalid duration format for process: {row['Process Name']}")
                continue
                
            # Map frequency to uppercase version
            frequency = FREQUENCY_MAPPING.get(row['Frequency'])
            if not frequency:
                logger.warning(f"Invalid frequency value: {row['Frequency']}")
                continue
                
            # Calculate computed fields
            yearly_volume = calculate_yearly_volume(row['Volume'], frequency)
            yearly_duration = calculate_yearly_duration(row['Duration'], yearly_volume)
            
            # Prepare record
            valid_record = {
                'email_id': row['Email ID'],
                'department': row['Team'],
                'process_name': row['Process Name'][:25],  # Truncate to 25 chars
                'description': row['Description'][:70] if pd.notna(row['Description']) else '',
                'apps_used': row['Apps Used'],
                'frequency': frequency,
                'duration': row['Duration'],
                'volume': row['Volume'],
                'yearly_volume': yearly_volume,
                'yearly_duration': yearly_duration,
                'process_status': row['Process Status'].upper(),
                'documentation': row['Documentation'] if pd.notna(row['Documentation']) else None
            }
            valid_records.append(valid_record)
        
        # Insert valid records
        cursor = conn.cursor()
        for record in valid_records:
            cursor.execute('''
            INSERT INTO processes (
                email_id, department, process_name, description, apps_used,
                frequency, duration, volume, yearly_volume, yearly_duration,
                process_status, documentation
            ) VALUES (
                :email_id, :department, :process_name, :description, :apps_used,
                :frequency, :duration, :volume, :yearly_volume, :yearly_duration,
                :process_status, :documentation
            )
            ''', record)
        
        conn.commit()
        logger.info(f"Imported {len(valid_records)} valid records")
        
    except (pd.errors.EmptyDataError, FileNotFoundError) as e:
        logger.error(f"Error reading CSV file: {e}")
        raise
    except sqlite3.Error as e:
        logger.error(f"Error importing data: {e}")
        raise

def main():
    """Main function to create database and import data."""
    try:
        logger.info("Starting database initialization")
        
        # Remove existing database if it exists
        if Path('processes.db').exists():
            Path('processes.db').unlink()
            logger.info("Removed existing database")
        
        # Create database and schema
        conn = create_database()
        
        # Import sample data
        import_sample_data(conn)
        
        # Verify data
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM processes")
        count = cursor.fetchone()[0]
        logger.info(f"Total records in database: {count}")
        
        conn.close()
        logger.info("Database initialization completed successfully")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise

if __name__ == "__main__":
    main()
