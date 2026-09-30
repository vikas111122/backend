from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "TLO_SUPER_SECRET_JWT_KEY_2026_CHANGE_IN_PRODUCTION"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120

settings = Settings()