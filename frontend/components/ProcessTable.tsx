/**
 * Process table component for displaying and managing processes.
 * 
 * @author Cline
 */

"use client";

import { useQuery } from "@tanstack/react-query";
import { Process, processApi } from "@/lib/api";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

interface ProcessTableProps {
  onCreateClick: () => void;
  onEditClick: (process: Process) => void;
  onDeleteClick: (id: number) => void;
}

export function ProcessTable({ onCreateClick, onEditClick, onDeleteClick }: ProcessTableProps) {
  // Fetch processes
  const { data, isLoading, error } = useQuery({
    queryKey: ["processes"],
    queryFn: () => processApi.list(),
  });

  if (isLoading) {
    return <div>Loading processes...</div>;
  }

  if (error) {
    return <div>Error loading processes</div>;
  }

  return (
    <Card className="w-full p-4">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold">Processes</h2>
        <Button onClick={onCreateClick}>Create Process</Button>
      </div>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Process Name</TableHead>
            <TableHead>Department</TableHead>
            <TableHead>Description</TableHead>
            <TableHead>Apps Used</TableHead>
            <TableHead>Frequency</TableHead>
            <TableHead>Status</TableHead>
            <TableHead>Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {data?.processes.map((process) => (
            <TableRow key={process.id}>
              <TableCell className="font-medium">{process.process_name}</TableCell>
              <TableCell>{process.department}</TableCell>
              <TableCell>{process.description}</TableCell>
              <TableCell>{process.apps_used}</TableCell>
              <TableCell>{process.frequency}</TableCell>
              <TableCell>
                <span
                  className={`px-2 py-1 rounded-full text-sm ${
                    process.process_status === "OPTIMIZED"
                      ? "bg-green-100 text-green-800"
                      : process.process_status === "STANDARDIZED"
                      ? "bg-blue-100 text-blue-800"
                      : "bg-yellow-100 text-yellow-800"
                  }`}
                >
                  {process.process_status}
                </span>
              </TableCell>
              <TableCell>
                <div className="flex gap-2">
                  <Button 
                    variant="outline" 
                    size="sm"
                    onClick={() => onEditClick(process)}
                  >
                    Edit
                  </Button>
                  <Button 
                    variant="outline" 
                    size="sm" 
                    className="text-red-600"
                    onClick={() => onDeleteClick(process.id!)}
                  >
                    Delete
                  </Button>
                </div>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </Card>
  );
}
