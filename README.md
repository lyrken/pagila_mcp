# Pagila MCP (Read-Only)

Servidor MCP desarrollado con FastMCP para consultar la base de datos Pagila (PostgreSQL)
de forma segura (solo lectura).

## Requisitos
- PostgreSQL 18 (o compatible)
- Base de datos: pagila (cargada)
- Python 3.x
- uv recomendado

## Instalación
```powershell
uv venv
.\.venv\Scripts\activate
uv pip install fastmcp "mcp[cli]" psycopg[binary] sqlparse
v

##VARIABLES DE ENTORNO

$env:PG_HOST="localhost"
$env:PG_PORT="5432"
$env:PG_DB="pagila"
$env:PG_USER="postgres"
$env:PG_PASS="TU_PASSWORD"

## Modelo relacional (Pagila)

La base de datos Pagila contiene 15 tablas principales, entre ellas:
actor, address, category, city, country, customer, film, film_actor, film_category,
inventory, language, payment, rental, staff, store.

Relaciones principales:
- rental se relaciona con inventory mediante inventory_id.
- inventory se relaciona con film mediante film_id.
- payment se relaciona con rental mediante rental_id.
- film_actor es una tabla puente (muchos a muchos) entre film y actor.
- film_category es una tabla puente (muchos a muchos) entre film y category.
- customer se relaciona con rental mediante customer_id.


//Lyrken Calle V.//