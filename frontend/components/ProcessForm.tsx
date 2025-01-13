/**
 * Form component for creating and editing processes.
 * 
 * @author Cline
 */

"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { Process } from "@/lib/api";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

// Form validation schema
const processSchema = z.object({
  email_id: z.string().email("Invalid email address"),
  department: z.enum(["AP", "AR", "GL", "Payroll"]),
  process_name: z.string().min(1).max(25),
  description: z.string().max(70).optional(),
  apps_used: z.string().min(1),
  frequency: z.enum([
    "DAILY",
    "WEEKLY",
    "BI_WEEKLY",
    "MONTHLY",
    "QUARTERLY",
    "YEARLY",
  ]),
  duration: z.string().regex(/^\d{2}:\d{2}$/, "Must be in HH:MM format"),
  volume: z.number().positive(),
  process_status: z.enum(["UNSTRUCTURED", "STANDARDIZED", "OPTIMIZED"]),
  documentation: z.string().optional(),
});

type ProcessFormData = z.infer<typeof processSchema>;

interface ProcessFormProps {
  initialData?: Process;
  onSubmit: (data: ProcessFormData) => void;
  onCancel: () => void;
}

export function ProcessForm({ initialData, onSubmit, onCancel }: ProcessFormProps) {
  const form = useForm<ProcessFormData>({
    resolver: zodResolver(processSchema),
    defaultValues: initialData || {
      email_id: "",
      department: "AP",
      process_name: "",
      description: "",
      apps_used: "",
      frequency: "DAILY",
      duration: "00:00",
      volume: 1,
      process_status: "UNSTRUCTURED",
      documentation: "",
    },
  });

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        <FormField
          control={form.control}
          name="email_id"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input {...field} type="email" placeholder="user@example.com" />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="department"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Department</FormLabel>
              <Select onValueChange={field.onChange} defaultValue={field.value}>
                <FormControl>
                  <SelectTrigger>
                    <SelectValue placeholder="Select department" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  {["AP", "AR", "GL", "Payroll"].map((dept) => (
                    <SelectItem key={dept} value={dept}>
                      {dept}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="process_name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Process Name</FormLabel>
              <FormControl>
                <Input {...field} placeholder="Enter process name" />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="description"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Description</FormLabel>
              <FormControl>
                <Textarea {...field} placeholder="Enter process description" />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="apps_used"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Apps Used</FormLabel>
              <FormControl>
                <Input {...field} placeholder="e.g., Excel, SAP" />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="frequency"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Frequency</FormLabel>
              <Select onValueChange={field.onChange} defaultValue={field.value}>
                <FormControl>
                  <SelectTrigger>
                    <SelectValue placeholder="Select frequency" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  {[
                    "DAILY",
                    "WEEKLY",
                    "BI_WEEKLY",
                    "MONTHLY",
                    "QUARTERLY",
                    "YEARLY",
                  ].map((freq) => (
                    <SelectItem key={freq} value={freq}>
                      {freq}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <FormMessage />
            </FormItem>
          )}
        />

        <div className="grid grid-cols-2 gap-4">
          <FormField
            control={form.control}
            name="duration"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Duration (HH:MM)</FormLabel>
                <FormControl>
                  <Input {...field} placeholder="00:30" />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="volume"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Volume</FormLabel>
                <FormControl>
                  <Input
                    {...field}
                    type="number"
                    min="1"
                    onChange={(e) => field.onChange(parseInt(e.target.value))}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>

        <FormField
          control={form.control}
          name="process_status"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Process Status</FormLabel>
              <Select onValueChange={field.onChange} defaultValue={field.value}>
                <FormControl>
                  <SelectTrigger>
                    <SelectValue placeholder="Select status" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  {["UNSTRUCTURED", "STANDARDIZED", "OPTIMIZED"].map((status) => (
                    <SelectItem key={status} value={status}>
                      {status}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="documentation"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Documentation</FormLabel>
              <FormControl>
                <Input {...field} placeholder="Documentation link or notes" />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <div className="flex justify-end gap-4">
          <Button type="button" variant="outline" onClick={onCancel}>
            Cancel
          </Button>
          <Button type="submit">
            {initialData ? "Update Process" : "Create Process"}
          </Button>
        </div>
      </form>
    </Form>
  );
}
