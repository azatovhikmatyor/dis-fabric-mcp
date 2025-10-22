import time
import struct
from datetime import datetime
from itertools import chain, repeat

from sqlalchemy import create_engine, Engine
from azure.identity import ClientSecretCredential

from app.core.config import Environment

env = Environment() # type: ignore


def get_connect_args(token):
    token_as_bytes = bytes(token, 'UTF-8')
    encoded_bytes = bytes(
        chain.from_iterable(zip(token_as_bytes, repeat(0)))
    )   # Encode the bytes to a Windows byte string
    token_bytes = (
        struct.pack('<i', len(encoded_bytes)) + encoded_bytes
    )   # Package the token into a bytes object
    attrs_before = {
        1256: token_bytes
    }  # Attribute pointing to SQL_COPT_SS_ACCESS_TOKEN to pass access token to the driver
    connect_args = {'attrs_before': attrs_before}
    return connect_args


class CachedEngine:
    def __init__(self):
        self.engine: Engine|None = None
        self.scope = 'https://database.windows.net/.default'
        self.buffer = 5*60 # 5 minutes

        self.WAREHOUSE_ID = env.warehouse_id
        self.DATABASE_NAME = env.database_name
        
        self.TENANT_ID = env.tenant_id
        self.CLIENT_ID = env.client_id
        self.CLIENT_SECRET = env.client_secret

        self.sql_endpoint = f'{self.WAREHOUSE_ID}.datawarehouse.fabric.microsoft.com'
        self.connection_string = f'Driver={{ODBC Driver 17 for SQL Server}};Server={self.sql_endpoint},1433;Database={self.DATABASE_NAME};Encrypt=Yes;TrustServerCertificate=No'

    def get_engine(self):
        if self.engine is None or self.token.expires_on < int(time.time()) + self.buffer:
            print('Issuing new token')
            self.credential = ClientSecretCredential(self.TENANT_ID, self.CLIENT_ID, self.CLIENT_SECRET) # type: ignore
            self.token = self.credential.get_token(self.scope)
            print('Token expires on', datetime.fromtimestamp(self.token.expires_on))

            connect_args = get_connect_args(self.token.token)
            self.engine = create_engine(
                'mssql+pyodbc:///?odbc_connect={0}'.format(self.connection_string),
                connect_args=connect_args,
            )
            return self.engine
        else:
            return self.engine


# import pandas as pd

# engine_manager = CachedEngine()

# engine = engine_manager.get_engine()

# from sqlalchemy import text
# with engine.connect() as conn:
#     sql = text('SELECT TABLE_CATALOG, TABLE_SCHEMA, TABLE_NAME, TABLE_TYPE FROM INFORMATION_SCHEMA.TABLES;')
#     result = conn.execute(sql)

#     rows = result.fetchall()

#     len(rows)

# start_time = time.perf_counter()
# sql = 'SELECT TABLE_CATALOG, TABLE_SCHEMA, TABLE_NAME, TABLE_TYPE FROM INFORMATION_SCHEMA.TABLES;'
# sql = 'SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES;'
# df = pd.read_sql(sql, engine_manager.get_engine())

# df
# end_time = time.perf_counter()
# print('duration:', end_time-start_time)

