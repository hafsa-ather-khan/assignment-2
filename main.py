from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from database import initialize_database, get_connection
app = FastAPI()

initialize_database()

# Optional: Using Pydantic for request body structure validation
class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

@app.get("/")
def read_root():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/tasks")
def get_all_tasks():
    connection = get_connection()

    rows = connection.execute(
        "SELECT * FROM tasks"
    ).fetchall()

    connection.close()

    return [
        {
            "id": row["id"],
            "title": row["title"],
            "done": bool(row["done"])
        }
        for row in rows
    ]

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    connection = get_connection()

    row = connection.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    connection.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail={"error": f"Task {task_id} not found"}
        )

    return {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"])
    }
# Stage 3: Create a new task with validation and 201 status code
@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task_data: dict):
    # Validate that 'title' exists and is not an empty string or just whitespace
    title = task_data.get("title")
    if not title or not title.strip():
        raise HTTPException(status_code=400, detail={"error": "Title is required and cannot be empty"})
    
    # Generate the next free ID automatically
    new_id = tasks[-1]["id"] + 1 if tasks else 1
    
    # Create the new task object
    new_task = {
        "id": new_id,
        "title": title.strip(),
        "done": False
    }
    
    # Add it to our in-memory list
    tasks.append(new_task)
    
    return new_task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_data: TaskUpdate):
    task = next((t for t in tasks if t["id"] == task_id), None)

    if not task:
        raise HTTPException(
            status_code=404,
            detail={"error": f"Task {task_id} not found"}
        )

    if task_data.title is None and task_data.done is None:
        raise HTTPException(
            status_code=400,
            detail={"error": "Request body cannot be empty"}
        )

    if task_data.title is not None:
        if not task_data.title.strip():
            raise HTTPException(
                status_code=400,
                detail={"error": "Title cannot be empty"}
            )
        task["title"] = task_data.title.strip()

    if task_data.done is not None:
        task["done"] = task_data.done

    return task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    task = next((t for t in tasks if t["id"] == task_id), None)

    if not task:
        raise HTTPException(
            status_code=404,
            detail={"error": f"Task {task_id} not found"}
        )

    tasks.remove(task)