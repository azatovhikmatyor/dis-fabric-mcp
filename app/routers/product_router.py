import pandas as pd
from itertools import permutations

from fastapi import APIRouter
from fastapi import Depends

from app.utils.cached_fabric_engine import CachedEngine
from app.utils.sql_loader import load_sql
from app.utils import verify_token


engine_manager = CachedEngine()

router = APIRouter()


@router.get('/find_product_code/{description}', operation_id='find_product_code')
async def find_product_code(description: str, token: str = Depends(verify_token)) -> str:
    """
    Use this tool to identify the most likely product code (SKU or model number) based on a partial product reference 
    such as a vague description, incomplete SKU, or general product name.

    Input:
        - query: A partial or descriptive reference to a product (e.g., "3-ton air handler", "ASPT unit", "14ACX").

    Behavior:
        - This tool returns several matching product candidates based on the input.
        - The AI must review the returned matches and select the most relevant product code.
        - Once selected, the product code should be used with the `get_frequently_bundled_products` tool to retrieve compatible items.

    Output:
        - A markdown list or table of the top matching product codes, including product code and description.
        - Ensure the response is clean and easy to parse for further decision-making.

    Only use this tool when the input product reference is not a clear or complete product code.
    Do NOT use this tool if a full and unambiguous SKU or model number is already provided.
    """

    sql_stmt = load_sql("product/find_product_code.sql")
    descriptions = description.lower().split()
    if len(description) == 1:
        condition = 'LOWER(PRODUCTDESC) LIKE %' + description.lower() + '%'
    else:
        combinations = list(permutations(descriptions, 2))

        condition = ' OR '.join(
            [
                'LOWER(PRODUCTDESC) LIKE ' + desc for desc in
                ["'%" + '%'.join(combination) + "%'" for combination in combinations]
            ]
        )

    sql_stmt = sql_stmt + ' WHERE ' + condition

    engine = engine_manager.get_engine()
    df = pd.read_sql(
        sql_stmt,
        engine,
    )
    return df.to_markdown()


# TODO: filter by Product Code + Customer 
@router.get('/get_frequently_bundled_products/{product_code}', operation_id='get_frequently_bundled_products')
async def get_frequently_bundled_products(product_code: str, token: str = Depends(verify_token)) -> str:
    """
    Use this tool to retrieve HVAC products that are frequently bundled or commonly purchased 
    together with the specified product.

    Input:
        - product_code: A specific and valid product code (SKU or model number).
          If the input is ambiguous or vague, first use the `find_product_code` tool to resolve it.

    Behavior:
        - Return a list of related HVAC products that are commonly bundled with the given product.
        - The tool should only be used when the product code is confidently identified.
        - If no relevant bundles are found, return a clear message indicating no results.

    ProductCode, ProductDescription and PercentageOfInvoicesContainTheProduct columns are important.

    Do NOT use this tool for general product lookup or ambiguous input.
    Ensure the input product code is specific and accurate before calling this tool.
    """
    sql_stmt = load_sql("product/get_frequently_bundled_products.sql")
    engine = engine_manager.get_engine()
    df = pd.read_sql(
        # sql_stmt,
        "select * from demo",
        engine,
        params=(product_code, product_code),
    )
    return df.to_markdown()
