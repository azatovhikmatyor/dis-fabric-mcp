from fastapi import FastAPI
from fastapi import Depends
from fastapi_mcp import FastApiMCP, AuthConfig

from app.utils import security
from app.routers.product_router import router as product_router
from app.routers.inventory_router import router as inventory_router
from app.routers.general_router import router as general_router

app = FastAPI()
app.include_router(product_router)
app.include_router(inventory_router)
app.include_router(general_router)

tool_names = [
    # from product router
    'find_product_code', 
    'get_frequently_bundled_products', 
    
    # from inventory router
    'ramaining_quantity',

    # from general router
    'tables',
    'schema_info',
    'query'
]


if __name__ == '__main__':
    import uvicorn

    mcp = FastApiMCP(
        app,
        include_operations=tool_names,
        auth_config=AuthConfig(
            dependencies=[Depends(security)],
        ),
    )
    mcp.mount(mount_path='/sse')
    uvicorn.run(app, host='0.0.0.0', port=8000)
