# FastAPI Task API

A simple RESTful Task API built with **FastAPI** and **Pydantic**.

This project implements a complete CRUD API for managing tasks using an in-memory task list.

## Features

* Create tasks
* Get all tasks
* Get a single task by ID
* Update a task's title and/or completion status
* Delete tasks
* Request validation with Pydantic
* Proper HTTP status codes
* Interactive Swagger API documentation

## Tech Stack

* **Python**
* **FastAPI**
* **Pydantic**
* **Uvicorn**

## Installation & Running

Clone the repository and navigate into the project directory.

Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install the dependencies:

```bash
pip install fastapi uvicorn
```

Run the API:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger UI is available at:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

| Method | Endpoint           | Description         | Success Status |
| ------ | ------------------ | ------------------- | -------------- |
| GET    | `/`                | Get API information | 200            |
| GET    | `/health`          | Check API health    | 200            |
| GET    | `/tasks`           | Get all tasks       | 200            |
| GET    | `/tasks/{task_id}` | Get a task by ID    | 200            |
| POST   | `/tasks`           | Create a new task   | 201            |
| PUT    | `/tasks/{task_id}` | Update a task       | 200            |
| DELETE | `/tasks/{task_id}` | Delete a task       | 204            |

## Example: Create a Task

```bash
curl -i -X POST http://127.0.0.1:8000/tasks -H "Content-Type: application/json" -d "{\"title\":\"Learn FastAPI\"}"
```

Example response:

```text
HTTP/1.1 201 Created
content-type: application/json

{"id":4,"title":"Learn FastAPI","done":false}
```

## Example: Get All Tasks

```bash
curl -i http://127.0.0.1:8000/tasks
```

## Example: Update a Task

```bash
curl -i -X PUT http://127.0.0.1:8000/tasks/4 -H "Content-Type: application/json" -d "{\"title\":\"Master FastAPI\",\"done\":true}"
```

## Example: Delete a Task

```bash
curl -i -X DELETE http://127.0.0.1:8000/tasks/4
```

The API returns:

```text
HTTP/1.1 204 No Content
```

## Error Handling

The API returns appropriate status codes for invalid requests and unknown task IDs.

| Status | Meaning                                                  |
| -----: | -------------------------------------------------------- |
|    200 | Request successful                                       |
|    201 | Task successfully created                                |
|    204 | Task successfully deleted; no response body              |
|    400 | Invalid or empty request data                            |
|    404 | Task ID not found                                        |
|    422 | Request body does not match the expected Pydantic schema |

## Swagger UI

FastAPI automatically provides interactive API documentation through Swagger UI.


<img width="1366" height="677" alt="637727294-40a8d907-4d16-4ecd-bccc-ce17e2dfedbd" src="https://github.com/user-attachments/assets/b88f40a6-f4d1-4245-8963-fed52dbb7356" />


## Project Structure

```text
fastapi-task-api/
├── main.py
├── README.md
├── swagger.png
└── .gitignore
```

## Storage

Tasks are currently stored in an **in-memory Python list**.

This means all tasks are reset when the application restarts. No external database is required for this project.

## Stage 4 — SQLite Exploration

I opened `tasks.db` using DB Browser for SQLite and ran the following SQL queries directly against the database.

### SQL Queries

#### 1. Select all tasks

```sql
SELECT * FROM tasks;
```

This query returned all tasks stored in the `tasks` table.

#### 2. Select completed tasks

```sql
SELECT * FROM tasks WHERE done = 1;
```

This query returned only the tasks that were marked as completed.

#### 3. Count all tasks

```sql
SELECT COUNT(*) FROM tasks;
```

This query returned the total number of tasks currently stored in the database.

#### 4. Mark all tasks as completed

```sql
UPDATE tasks SET done = 1;
```

This query changed the `done` value of every task to `1`, marking all tasks as completed.

#### 5. Delete completed tasks

```sql
DELETE FROM tasks WHERE done = 1;
```

This query deleted all tasks whose `done` value was `1`.

### Database Browser Screenshot
<img width="588" height="645" alt="image (16)" src="https://github.com/user-attachments/assets/dc0d1497-54ad-4e29-8d73-89e090632b55" />



The changes made directly in DB Browser were reflected immediately by the FastAPI `/tasks` endpoint because both the API and DB Browser use the same `tasks.db` database file.

## Stage 5 — Publish Your Database Project

### Why SQLite?

SQLite was chosen because it is lightweight, requires no separate database server, uses a single database file, and provides persistent storage for the application. It is simple to set up and is well suited for this task management API.

### Database File

The SQLite database is stored in:

```text
tasks.db
```

The file is created automatically when the application starts if it does not already exist. The `tasks` table and the three initial example tasks are also created automatically when needed.

The `tasks.db` file is excluded from Git using `.gitignore`, so anyone cloning the repository starts with a fresh database that is automatically initialized by the application.

### How to Start the Project

1. Clone the repository.

2. Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Start the FastAPI server:

```bash
uvicorn main:app --reload
```

5. Open the API documentation:

```text
http://127.0.0.1:8000/docs
```

The `tasks.db` database is created automatically when the application starts.



### Clean Clone Checkpoint

The project does not require manual database setup. After cloning the repository and running the documented start command, `tasks.db` is automatically created, the `tasks` table is initialized, and the three example tasks are seeded when the database is empty.



## Project Status

🎉 Complete CRUD API implemented and published as part of the FastAPI internship assignments.
