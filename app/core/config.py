import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

class Settings(BaseSettings):
    # Pega o valor, remove espaços em branco das pontas, e tira aspas caso existam
    admin_user: str = os.getenv("ADMIN_USER", "victor").strip().replace('"', '').replace("'", "")
    admin_password: str = os.getenv("ADMIN_PASSWORD", "frete2026").strip().replace('"', '').replace("'", "")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./frete.db").strip().replace('"', '')

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()