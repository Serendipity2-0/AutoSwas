import Database from 'better-sqlite3';
import path from 'path';

/**
 * Interface for finance task data
 */
export interface FinanceTask {
  Email: string;
  EmployeeID: string;
  Department: string;
  SubDepartment: string;
  TaskName: string;
  TaskDescription: string;
  Tools: string;
  Frequency: string;
  Duration: number;
  DailyOccurrence: number;
  MonthlyTime: string;
  Complexity: string;
  Maturity: string;
  AutomationPotential: string;
  AutomationTool: string;
}

/**
 * Database service for finance tasks
 */
export class FinanceDB {
  private db: Database.Database;

  constructor() {
    const dbPath = path.join(process.cwd(), 'finance_tasks.db');
    this.db = new Database(dbPath);
    console.log('Connected to database:', dbPath);
  }

  /**
   * Get all finance tasks
   */
  getAllTasks(): FinanceTask[] {
    const stmt = this.db.prepare('SELECT * FROM finance_tasks');
    return stmt.all() as FinanceTask[];
  }

  /**
   * Add a new finance task
   */
  addTask(task: Omit<FinanceTask, 'MonthlyTime' | 'Unknown'>): void {
    const stmt = this.db.prepare(`
      INSERT INTO finance_tasks (
        Email, EmployeeID, Department, SubDepartment, TaskName,
        TaskDescription, Tools, Frequency, Duration, DailyOccurrence,
        Complexity, Maturity, AutomationPotential, AutomationTool
      ) VALUES (
        @Email, @EmployeeID, @Department, @SubDepartment, @TaskName,
        @TaskDescription, @Tools, @Frequency, @Duration, @DailyOccurrence,
        @Complexity, @Maturity, @AutomationPotential, @AutomationTool
      )
    `);
    
    stmt.run(task);
  }
}

// Export singleton instance
export const db = new FinanceDB();
