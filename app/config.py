from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    is_development: bool = True
    is_local: bool = False
    fastapi_port: int = 8080
    access_token_expiry: int = 30
    refresh_token_expiry: int = 60 * 24 * 7
    basic_auth_password: str
    secret_key: str
    algorithm: str
    security_password_salt: str
    database_host: str
    database_port: int = 5432
    database_username: str
    database_password: str
    database_name: str


settings = Settings()
