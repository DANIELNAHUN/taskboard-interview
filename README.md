# TaskBoard

Pequeña app de tareas: backend FastAPI + SQLite, frontend en HTML/JS plano.

## Arranque

```bash
pip install -r requirements.txt
python scripts/seed.py          # crea 25 tareas de ejemplo
uvicorn app.main:app --reload   # abre http://localhost:8000
pytest                          # tests existentes
```

## Estructura

- `app/main.py` — API
- `static/` — frontend
- `tests/` — tests
- `review/export_report.py` — módulo pendiente de revisión (no está conectado a la app)

## La prueba (30 min)

Puedes usar IA, Google y la documentación que quieras. Comparte pantalla y piensa en voz alta.

1. **Bug (≈8 min).** Un usuario reporta: *"Cuando tengo muchas tareas, algunas no aparecen y la paginación se comporta raro, sobre todo al filtrar."* Encuéntralo y arréglalo.
2. **Feature (≈12 min).** Añade un campo `priority` (`low` / `medium` / `high`, por defecto `medium`) a las tareas: base de datos, API y que se vea y se pueda elegir en la interfaz.
3. **Code review (≈10 min).** Revisa `review/export_report.py` como si fuera una PR de un compañero. Dinos qué cambiarías y por qué.
