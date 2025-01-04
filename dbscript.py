import pandas as pd
import sqlite3
from pathlib import Path

def create_finance_db():
    # Read the CSV file
    df = pd.read_csv('Sample Data1.csv', header=None, 
                     names=['Email', 'EmployeeID', 'Department', 'SubDepartment', 
                           'TaskName', 'TaskDescription', 'Tools', 'Frequency',
                           'Duration', 'DailyOccurrence', 'MonthlyTime', 
                           'Complexity', 'Maturity', 'Unknown', 'AutomationPotential',
                           'AutomationTool'])

    # Create SQLite database
    conn = sqlite3.connect('finance_tasks.db')
    
    # Convert DataFrame to SQL table
    df.to_sql('finance_tasks', conn, if_exists='replace', index=False)
    
    # Create indexes for commonly queried fields
    cursor = conn.cursor()
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_employee ON finance_tasks(EmployeeID)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_department ON finance_tasks(Department, SubDepartment)')
    
    # Commit and close connection
    conn.commit()
    conn.close()
    
    print("Database created successfully!")
    
    # Verify the data
    conn = sqlite3.connect('finance_tasks.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM finance_tasks")
    count = cursor.fetchone()[0]
    print(f"Total records in database: {count}")
    conn.close()

if __name__ == "__main__":
    create_finance_db()