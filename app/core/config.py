"""
Application configuration using pydantic-settings.
All secrets are loaded from environment variables / .env file.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # App / institute identity
    APP_NAME: str = "NextGen Institute Educational ERP API"
    APP_VERSION: str = "1.0.0"
    INSTITUTION_NAME: str = "NextGen Institute of AI & Technology"
    INSTITUTION_SHORT: str = "NGIAT"
    SERVICE_NAME: str = "nextgen-edu-api"
    ENVIRONMENT: str = "development"

    # Database — must be set via env var in production (Render internal connection string)
    DATABASE_URL: str = "postgresql+psycopg://user:password@localhost:5432/ngiat_erp"

    # Authentication credentials — NEVER hardcode production values
    BEARER_TOKEN: str = "EDU-BEARER-2026-TEST"
    API_KEY: str = "EDU-APIKEY-2026-TEST"
    BASIC_USERNAME: str = "audit_admin"
    BASIC_PASSWORD: str = "EduPassword@2026"

    # Logging
    LOG_LEVEL: str = "INFO"

    # Rate limiting (requests per minute per IP)
    RATE_LIMIT_PER_MINUTE: int = 100

    # Pagination defaults
    DEFAULT_PAGE_SIZE: int = 100
    MAX_PAGE_SIZE: int = 1000

    # CORS
    CORS_ORIGINS: list[str] = ["*"]

    # Dataset size for seeding: small=1000, medium=10000, large=50000, xl=100000
    # Can also be overridden by SEED_STUDENTS directly
    DATASET_SIZE: str = "medium"
    SEED_STUDENTS: int = 0   # if > 0 takes priority over DATASET_SIZE


settings = Settings()

# Resolve effective student target from DATASET_SIZE or SEED_STUDENTS
DATASET_SIZE_MAP = {
    "small": 1_000,
    "medium": 10_000,
    "large": 50_000,
    "xl": 100_000,
}


def get_student_target() -> int:
    if settings.SEED_STUDENTS > 0:
        return settings.SEED_STUDENTS
    return DATASET_SIZE_MAP.get(settings.DATASET_SIZE.lower(), 10_000)
