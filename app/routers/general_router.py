import pandas as pd

from fastapi import APIRouter
from fastapi import Depends, Path, HTTPException

from app.utils.cached_fabric_engine import CachedEngine
from app.utils import verify_token


engine_manager = CachedEngine()

router = APIRouter()


@router.get('/tables', operation_id='tables')
async def get_tables(token: str = Depends(verify_token)) -> str:
    """
    Use this tool to list all available tables in the connected Microsoft Fabric warehouse.
    This should be the first tool you call when trying to understand what data is available.
    """
    sql = 'SELECT TABLE_SCHEMA, TABLE_NAME, TABLE_TYPE FROM INFORMATION_SCHEMA.TABLES'

    df = pd.read_sql(sql, engine_manager.get_engine())
    return df.to_json(orient='split', index=False)


@router.get('/schema_info/{schema_name}/{table_name}', operation_id='schema_info')
async def get_schema_info(
    schema_name: str = Path(
        ..., description='Schema of the table to retrieve column details for'
    ),
    table_name: str = Path(
        ..., description='Name of the table without schema to retrieve column details for'
    ),
    token: str = Depends(verify_token),
) -> str:
    """
    Use this tool to get the list of columns and their data types for a specific table.
    Call this after identifying the table name using the `/tables` tool.
    This is necessary before writing any SQL queries.
    Table name must be given
    """
    sql = 'SELECT TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = ? AND TABLE_NAME = ?'

    df = pd.read_sql(
        sql,
        engine_manager.get_engine(),
        params=(schema_name, table_name,),
    )
    return df.to_json(orient='split', index=False)


@router.get('/query/{query}', operation_id='query')
async def query(query: str, token: str = Depends(verify_token)) -> str:
    """
    Use this tool to run a SELECT query after you have confirmed the table and column names.
    Do not use this tool until you have reviewed the schema with `/tables` and `/schema_info`.
    This tool executes read-only SQL queries and returns results in markdown format.
    The query must be valid T-SQL query. Do not use non T-SQL statements e.g. LIKE.
    Keep in mind that Fabric is case-sensitive.
    """
    try:
        df = pd.read_sql(query, engine_manager.get_engine())
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"SQL execution error: {str(e)}")
    
    return df.to_json(orient='split', index=False)
