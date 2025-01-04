import { NextResponse } from 'next/server';
import { db } from '../../../lib/db';

/**
 * GET handler for retrieving all tasks
 */
export async function GET() {
  try {
    const tasks = db.getAllTasks();
    return NextResponse.json(tasks);
  } catch (error) {
    console.error('Failed to fetch tasks:', error);
    return NextResponse.json(
      { error: 'Failed to fetch tasks' },
      { status: 500 }
    );
  }
}

/**
 * POST handler for creating a new task
 */
export async function POST(request: Request) {
  try {
    const task = await request.json();
    db.addTask(task);
    const tasks = db.getAllTasks(); // Return updated list
    return NextResponse.json(tasks);
  } catch (error) {
    console.error('Failed to add task:', error);
    return NextResponse.json(
      { error: 'Failed to add task' },
      { status: 500 }
    );
  }
}
