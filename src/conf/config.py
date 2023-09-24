from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    sqlalchemy_database_url: str = "postgresql+asyncpg://postgres:password@localhost:5432/postgres"
    jwt_secret_key: str = "secret"
    jwt_algorithm: str = "HS256"
    mail_username: str = "example@mail.com"
    mail_password: str = "password"
    mail_from: str = "example@mail.com"
    mail_port: int = 123
    mail_server: str = "smtp.mail.com"
    redis_host: str = "localhost"
    redis_password: str = "password"
    redis_port: int = 6379
    # cloudinary_name: str = "name"
    # cloudinary_api_key: str = "123456"
    # cloudinary_api_secret: str = "secret"

    model_config = ConfigDict(extra='ignore', env_file=".env", env_file_encoding="utf-8")


settings = Settings()
