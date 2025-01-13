/**
 * Main page component for process management.
 * Handles process listing, creation, and updates.
 * 
 * @author Cline
 */

"use client";

import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { ProcessTable } from "@/components/ProcessTable";
import { ProcessForm } from "@/components/ProcessForm";
import { Process, processApi } from "@/lib/api";
import { Card } from "@/components/ui/card";

type Mode = "list" | "create" | "edit";

export default function Home() {
  const [mode, setMode] = useState<Mode>("list");
  const [selectedProcess, setSelectedProcess] = useState<Process | undefined>();
  const queryClient = useQueryClient();

  // Create process mutation
  const createMutation = useMutation({
    mutationFn: processApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["processes"] });
      setMode("list");
    },
  });

  // Update process mutation
  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<Process> }) =>
      processApi.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["processes"] });
      setMode("list");
      setSelectedProcess(undefined);
    },
  });

  // Delete process mutation
  const deleteMutation = useMutation({
    mutationFn: processApi.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["processes"] });
    },
  });

  const handleCreate = () => {
    setSelectedProcess(undefined);
    setMode("create");
  };

  const handleEdit = (process: Process) => {
    setSelectedProcess(process);
    setMode("edit");
  };

  const handleDelete = async (id: number) => {
    if (confirm("Are you sure you want to delete this process?")) {
      await deleteMutation.mutateAsync(id);
    }
  };

  const handleCancel = () => {
    setMode("list");
    setSelectedProcess(undefined);
  };

  return (
    <main className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        {mode === "list" ? (
          <ProcessTable
            onCreateClick={handleCreate}
            onEditClick={handleEdit}
            onDeleteClick={handleDelete}
          />
        ) : (
          <Card className="p-6">
            <h1 className="text-2xl font-bold mb-6">
              {mode === "create" ? "Create Process" : "Edit Process"}
            </h1>
            <ProcessForm
              initialData={selectedProcess}
              onSubmit={async (data) => {
                if (mode === "create") {
                  await createMutation.mutateAsync(data);
                } else if (selectedProcess?.id) {
                  await updateMutation.mutateAsync({
                    id: selectedProcess.id,
                    data,
                  });
                }
              }}
              onCancel={handleCancel}
            />
          </Card>
        )}
      </div>
    </main>
  );
}
