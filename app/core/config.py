from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(BaseSettings):
    warehouse_id: str
    database_name: str
    tenant_id: str
    client_id: str
    client_secret: str
    mcp_auth_token: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")