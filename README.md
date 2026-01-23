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

//Lyrken Calle V.//