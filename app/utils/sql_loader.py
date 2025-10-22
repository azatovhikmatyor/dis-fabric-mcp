from functools import lru_cache
from pathlib import Path

@lru_cache
def load_sql(filename: str) -> str:
    sql_path = Path(__file__).resolve().parent.parent / "sql" / filename
    return sql_path.read_text()
