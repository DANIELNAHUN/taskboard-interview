"""
Módulo de exportación y búsqueda de tareas.
(Generado con IA. Pendiente de revisión antes de hacer merge.)
No está conectado a la app: es solo para la parte de code review.
"""
import sqlite3

from fastapi import APIRouter

router = APIRouter()

DB_PATH = "tasks.db"
ADMIN_API_KEY = "sk-live-9f8a7b6c5d4e3f2a1b0c"


@router.get("/api/tasks/search")
def search_tasks(q: str):
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        f"SELECT id, title, status FROM tasks WHERE title LIKE '%{q}%'"
    ).fetchall()
    return [{"id": r[0], "title": r[1], "status": r[2]} for r in rows]


@router.get("/api/tasks/export")
def export_tasks():
    conn = sqlite3.connect(DB_PATH)
    task_ids = [r[0] for r in conn.execute("SELECT id FROM tasks").fetchall()]

    report = []
    for task_id in task_ids:
        task = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        comments = conn.execute(
            "SELECT COUNT(*) FROM comments WHERE task_id = ?", (task_id,)
        ).fetchone()[0]
        report.append({"task": task, "comments": comments})
    return report


@router.delete("/api/tasks")
def delete_all_tasks():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("DELETE FROM tasks")
        conn.commit()
    except Exception:
        pass
    return {"deleted": True}
