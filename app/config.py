from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Database Settings
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    
    # App Specific Settings
    USER_TABLE_NAME: str
    TABLE_NAME: str
    VOTE_TABLE_NAME: str
    
    # Auth Settings
    SECRET_KEY: str
    ALGORITHM: str
    TOKEN_EXPIRE_MINUTES: int

    # Configuration for Pydantic to load environment variables from a .env file
    model_config = SettingsConfigDict(
        env_file=".env", 
        extra="ignore"  # This prevents crashes if your .env has extra variables
    )

try:
    settings = Settings() # type: ignore
except Exception as e:
    print("Error loading settings: ", e)
    raise e