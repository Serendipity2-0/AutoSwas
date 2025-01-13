Process Table: Data Types and Descriptions 

1. Email ID:  
   - Data Type: 'VARCHAR' (Email)  
   - Example: 'user@example.com'  
   - Description: Email address of the user or admin responsible for the process, as per admin input.  

2. Department (Dept):  
   - Data Type: 'ENUM' (Single Select)  
   - Example: 'HR', 'IT', 'Finance'  
   - Description: Name of the department, selected from a predefined list, as per admin input.  

3. Process Name:  
   - Data Type: 'VARCHAR(25)'  
   - Example: 'Invoice Processing'  
   - Description: Short name for the process, limited to 25 characters, as per user input.  

4. Description:  
   - Data Type: 'VARCHAR(70)'  
   - Example: 'Handles invoices'  
   - Description: Brief description of the process, limited to 70 characters, as per user input.  

5. Apps Used:  
   - Data Type: 'ENUM' (Single Select)  
   - Example: 'Excel', 'SAP', 'Salesforce'  
   - Description: Name of the application used for the process, selected from a predefined list, as per user input.  

6. Frequency:  
   - Data Type: 'ENUM' (Single Select)  
   - Example: 'Daily', 'Weekly', 'Monthly'  
   - Description: Frequency at which the process occurs, selected from predefined options: 'Daily', 'Weekly', 'Bi-Weekly', 'Monthly', 'Quarterly', 'Yearly'.  

7. Duration:  
   - Data Type: 'TIME' (HH:MM)  
   - Example: '2 hrs 30 mins', '15 mins'  
   - Description: Average duration of the process in hours and minutes for a single occurrence. For zero hours, mention only minutes.  

8. Volume:  
   - Data Type: 'INT'  
   - Example: '50'  
   - Description: Volume of occurrences per process frequency (e.g., 50 invoices per week).  

9. Yearly Volume:  
   - Data Type: 'INT'  
   - Example: '2400'  
   - Description: Computed field: Volume multiplied by annual frequency factor ('Daily=220', 'Weekly=48', 'Bi-Weekly=24', 'Monthly=12', 'Quarterly=4', 'Yearly=1').  

10. Yearly Duration:  
    - Data Type: 'TIME' (HH:MM)  
    - Example: '25 hrs 30 mins'  
    - Description: Computed field: Total yearly duration in hours and minutes, derived from 'Duration * Yearly Volume'. Round minutes to the nearest 5 minutes.  

11. Process Status:  
    - Data Type: 'ENUM' (Single Select)  
    - Example: 'Non-Standardised', 'Standardized', 'Optimized', 
    - Description: Indicates the process maturity:  
      - *Semi-Standardized*: Variability in execution.  
      - *Standardized*: Fully defined and consistently executed.  
      - *Optimized*: Improved for efficiency, with bottlenecks removed.  

12. Documentation:   
    - Data Type: Docs , PDFs, images. 

____________________________________________________________________________________________________ 

Notes for Implementation

1. Data Validation:  
   - Ensure 'Email ID' follows a valid email format.  
   - Validate time fields ('Duration', 'Yearly Duration') to accept only valid time formats.  

2. Predefined Lists:  
   - Use lookup tables or enums for fields like 'Department', 'Apps Used', 'Frequency', 'Process Status'. Use unique values from these columns for Enum constants. 

3. Computed Fields:  
   - Yearly Volume: Calculated based on 'Frequency' and 'Volume'.  
   - Yearly Duration: Calculated as 'Duration * Yearly Volume', with results rounded to the nearest 5 minutes.  
This refined version maintains consistency, corrects formatting, and aligns with the requirement that all 'ENUM' fields are single select. Let me know if further adjustments are needed!
