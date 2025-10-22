import pandas as pd

from fastapi import APIRouter
from fastapi import Depends

from app.utils.cached_fabric_engine import CachedEngine
from app.utils.sql_loader import load_sql
from app.utils import verify_token


engine_manager = CachedEngine()

router = APIRouter()


@router.get('/ramaining_quantity/{product_code}', operation_id='ramaining_quantity')
async def find_product_code(product_code: str, token: str = Depends(verify_token)) -> str:
    """
    Tool to find how many quantities of specific product are there in warehouses.
    """
    sql = load_sql('inventory/get_remaining_quantity.sql')

    df = pd.read_sql(
        sql,
        engine_manager.get_engine(),
        params=(product_code.lower(),),
    )
    return df.to_markdown()