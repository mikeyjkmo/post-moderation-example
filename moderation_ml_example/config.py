from pydantic import BaseSettings, Field, AnyHttpUrl


class Config(BaseSettings):
    CONTENT_MODERATION_SERVICE_URL: AnyHttpUrl = Field(
        default='http://localhost:5000',
        env='CONTENT_MODERATION_SERVICE_URL',
    )


config = Config()
