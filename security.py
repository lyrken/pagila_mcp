import re
import sqlparse

FORBIDDEN = {"INSERT","UPDATE","DELETE","DROP","ALTER","TRUNCATE","CREATE","GRANT","REVOKE"}

def is_safe_select(sql: str) -> bool:
    if not sql or len(sql) > 2000:
        return False

    parsed = sqlparse.parse(sql)
    if not parsed:
        return False

    stmt = parsed[0]
    if stmt.get_type() != "SELECT":
        return False

    # Evitar multi-sentencias
    if ";" in sql.strip().rstrip(";"):
        return False

    upper = sql.upper()
    for word in FORBIDDEN:
        if re.search(rf"\b{word}\b", upper):
            return False

    return True
