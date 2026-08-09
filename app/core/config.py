from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application Settings, managed by pydantic-settings.
    Values are overridden by environment variables (e.g. export APP_ENV=production).
    For local development, values are loaded from a .env file if it exists.
    """

    APP_ENV: str = "development"
    APP_NAME: str = "Employee Management API"
    APP_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    LOG_LEVEL: str = "INFO"

    # Database Settings
    DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


# Instantiate the settings object
settings = Settings()  # type: ignore
