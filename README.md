from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "your_super_secret_jwt_key_here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # MS SQL Server Database Credentials
    DB_SERVER: str = "localhost"  # or "localhost\\SQLEXPRESS" or your IP
    DB_NAME: str = "tlo_db"
    DB_USER: str = "sa"
    DB_PASSWORD: str = "YourStrongPassword123"

    @property
    def DATABASE_URL(self) -> str:
        # Uses pyodbc driver with ODBC Driver 18 for SQL Server
        return (
            f"mssql+pyodbc://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_SERVER}/{self.DB_NAME}?"
            f"driver=ODBC+Driver+18+for+SQL+Server&Encrypt=no"
        )

    class Config:
        env_file = ".env"

settings = Settings()
