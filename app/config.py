from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

class Settings(BaseSettings):
    db_host: str
    db_port: str
    db_name: str
    db_schema: str
    db_username: str
    db_password: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


    # Tell python where to get the env variables from
    # class Config:
    #    env_file = ".env"
    model_config = SettingsConfigDict(env_file=".env")  # <- v2 way

load_dotenv(".env")  # force load before Settings()
settings = Settings()
#print("SETTINGS ARE", settings.model_dump())