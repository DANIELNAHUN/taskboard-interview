import os
import sqlite3
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(title="TaskBoard")


def db_path() -> str:
    return os.environ.get("TASKBOARD_DB", str(BASE_DIR / "tasks.db"))


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(db_path())
    conn.row_factory = sqlite3.Row
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL DEFAULT '',
            status TEXT NOT NULL DEFAULT 'todo',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    return conn


class TaskCreate(BaseModel):
    title: str
    description: str = ""


@app.get("/api/tasks")
def list_tasks(status: str | None = None, page: int = 1, page_size: int = 10):
    where, params = "", []
    if status:
        where = "WHERE status = ?"
        params.append(status)

    offset = page * page_size

    with get_conn() as conn:
        rows = conn.execute(
            f"SELECT * FROM tasks {where} ORDER BY id LIMIT ? OFFSET ?",
            params + [page_size, offset],
        ).fetchall()
        total = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]

    return {
        "items": [dict(r) for r in rows],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@app.post("/api/tasks", status_code=201)
def create_task(task: TaskCreate):
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO tasks (title, description) VALUES (?, ?)",
            (task.title, task.description),
        )
        row = conn.execute("SELECT * FROM tasks WHERE id = ?", (cur.lastrowid,)).fetchone()
    return dict(row)


@app.patch("/api/tasks/{task_id}/toggle")
def toggle_task(task_id: int):
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Task not found")
        new_status = "done" if row["status"] == "todo" else "todo"
        conn.execute("UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id))
        return {**dict(row), "status": new_status}


@app.delete("/api/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    with get_conn() as conn:
        cur = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Task not found")


app.mount("/", StaticFiles(directory=BASE_DIR / "static", html=True), name="static")
