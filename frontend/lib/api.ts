/**
 * API client for communicating with the backend.
 * Handles all HTTP requests to the process management API.
 * 
 * @author Cline
 */

import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
});

export interface Process {
  id?: number;
  email_id: string;
  department: 'AP' | 'AR' | 'GL' | 'Payroll';
  process_name: string;
  description?: string;
  apps_used: string;
  frequency: 'DAILY' | 'WEEKLY' | 'BI_WEEKLY' | 'MONTHLY' | 'QUARTERLY' | 'YEARLY';
  duration: string;
  volume: number;
  yearly_volume?: number;
  yearly_duration?: string;
  process_status: 'UNSTRUCTURED' | 'STANDARDIZED' | 'OPTIMIZED';
  documentation?: string;
  created_at?: string;
  updated_at?: string;
}

export interface ProcessListResponse {
  processes: Process[];
  total: number;
}

/**
 * Process management API functions
 */
export const processApi = {
  /**
   * Get a list of all processes with optional filtering
   */
  list: async (params?: { 
    skip?: number; 
    limit?: number;
    department?: string;
    status?: string;
  }) => {
    const response = await api.get<ProcessListResponse>('/processes/', { params });
    return response.data;
  },

  /**
   * Get a single process by ID
   */
  get: async (id: number) => {
    const response = await api.get<Process>(`/processes/${id}`);
    return response.data;
  },

  /**
   * Create a new process
   */
  create: async (process: Omit<Process, 'id' | 'created_at' | 'updated_at'>) => {
    const response = await api.post<Process>('/processes/', process);
    return response.data;
  },

  /**
   * Update an existing process
   */
  update: async (id: number, process: Partial<Process>) => {
    const response = await api.put<Process>(`/processes/${id}`, process);
    return response.data;
  },

  /**
   * Delete a process
   */
  delete: async (id: number) => {
    await api.delete(`/processes/${id}`);
  },

  /**
   * Upload CSV file for bulk process import
   */
  uploadCsv: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post('/processes/upload-csv', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
};
