# AutoSwas Process Management System

A comprehensive system for managing and tracking business processes, their automation status, and related metrics.

## Features

- Process management with CRUD operations
- CSV data import functionality
- Computed metrics (yearly volume and duration)
- Data validation and sanitization
- RESTful API with FastAPI
- SQLite database for data persistence

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── models/
│   │   │   └── database.py
│   │   ├── routers/
│   │   │   └── process.py
│   │   ├── schemas/
│   │   │   └── process.py
│   │   └── main.py
│   └── requirements.txt
├── processes.db
├── dbscript.py
├── SampleData.csv
└── README.md
```

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd AutoSwas
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. Initialize the database:
   ```bash
   cd ..  # Return to root directory
   python dbscript.py
   ```

5. Start the FastAPI server:
   ```bash
   cd backend
   python -m uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- Interactive API documentation: `http://localhost:8000/docs`
- Alternative API documentation: `http://localhost:8000/redoc`

### Key Endpoints

- `GET /api/processes`: List all processes
- `POST /api/processes`: Create a new process
- `GET /api/processes/{id}`: Get a specific process
- `PUT /api/processes/{id}`: Update a process
- `DELETE /api/processes/{id}`: Delete a process
- `POST /api/processes/upload-csv`: Upload processes from CSV

## Data Model

### Process

- `email_id`: Email of process owner
- `department`: Department (AP, AR, GL, Payroll)
- `process_name`: Name of the process (max 25 chars)
- `description`: Process description (max 70 chars)
- `apps_used`: Applications used in the process
- `frequency`: Process frequency (Daily, Weekly, etc.)
- `duration`: Time taken (HH:MM format)
- `volume`: Number of occurrences per frequency
- `yearly_volume`: Computed yearly volume
- `yearly_duration`: Computed yearly duration
- `process_status`: Current status (Unstructured, Standardized, Optimized)
- `documentation`: Optional documentation links/notes

## Development

### Running Tests

```bash
cd backend
pytest
```

### Code Style

The project follows PEP 8 style guidelines. Key points:
- Use 4 spaces for indentation
- Maximum line length of 88 characters
- Docstrings for all public modules, functions, classes, and methods

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
