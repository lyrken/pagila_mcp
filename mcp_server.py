from fastmcp import FastMCP
from db import run_select
from security import is_safe_select
import json
from datetime import datetime

mcp = FastMCP("Pagila MCP (Read-Only)")

def log_event(event: str, payload: dict):
    print(json.dumps({
        "ts": datetime.utcnow().isoformat(),
        "event": event,
        "payload": payload
    }, ensure_ascii=False))

@mcp.tool()
def descubrir_tablas() -> dict:
    q = """
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema='public'
    ORDER BY table_name
    """
    rows = run_select(q)
    return {"tables": [r["table_name"] for r in rows]}

@mcp.tool()
def descubrir_columnas(tabla: str) -> dict:
    q = """
    SELECT column_name, data_type
    FROM information_schema.columns
    WHERE table_schema='public' AND table_name=%s
    ORDER BY ordinal_position
    """
    rows = run_select(q, (tabla,))
    return {"table": tabla, "columns": rows}

@mcp.tool()
def select_controlado(sql: str) -> dict:
    log_event("request_sql", {"sql": sql})

    if not is_safe_select(sql):
        log_event("blocked_sql", {"sql": sql})
        return {"ok": False, "error": "Consulta no permitida. Solo SELECT seguro."}

    try:
        rows = run_select(sql)
        return {"ok": True, "count": len(rows), "rows": rows}
    except Exception as e:
        log_event("sql_error", {"sql": sql, "error": str(e)})
        return {"ok": False, "error": str(e)}

@mcp.tool()
def peliculas_mas_alquiladas(top: int = 10) -> dict:
    q = """
    SELECT f.title, COUNT(*) AS rentals
    FROM rental r
    JOIN inventory i ON r.inventory_id = i.inventory_id
    JOIN film f ON i.film_id = f.film_id
    GROUP BY f.title
    ORDER BY rentals DESC
    LIMIT %s
    """
    rows = run_select(q, (top,))
    return {"metric": "peliculas_mas_alquiladas", "top": top, "rows": rows}

@mcp.tool()
def categorias_mayor_ingreso(top: int = 10) -> dict:
    q = """
    SELECT c.name AS categoria, SUM(p.amount) AS ingresos
    FROM payment p
    JOIN rental r ON p.rental_id = r.rental_id
    JOIN inventory i ON r.inventory_id = i.inventory_id
    JOIN film_category fc ON i.film_id = fc.film_id
    JOIN category c ON fc.category_id = c.category_id
    GROUP BY c.name
    ORDER BY ingresos DESC
    LIMIT %s
    """
    rows = run_select(q, (top,))
    return {"metric": "categorias_mayor_ingreso", "top": top, "rows": rows}

@mcp.tool()
def clientes_mas_activos(top: int = 10) -> dict:
    q = """
    SELECT cu.customer_id, cu.first_name, cu.last_name, COUNT(r.rental_id) AS rentals
    FROM customer cu
    JOIN rental r ON cu.customer_id = r.customer_id
    GROUP BY cu.customer_id, cu.first_name, cu.last_name
    ORDER BY rentals DESC
    LIMIT %s
    """
    rows = run_select(q, (top,))
    return {"metric": "clientes_mas_activos", "top": top, "rows": rows}

@mcp.tool()
def actores_mas_frecuentes(top: int = 10) -> dict:
    q = """
    SELECT a.first_name, a.last_name, COUNT(fa.film_id) AS peliculas
    FROM actor a
    JOIN film_actor fa ON a.actor_id = fa.actor_id
    GROUP BY a.first_name, a.last_name
    ORDER BY peliculas DESC
    LIMIT %s
    """
    rows = run_select(q, (top,))
    return {"metric": "actores_mas_frecuentes", "top": top, "rows": rows}

app = mcp
if __name__ == "__main__":
    mcp.run()

