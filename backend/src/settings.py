from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra='ignore')

    mosquitto_host: str = "broker"
    mosquitto_user: str
    mosquitto_password: str
    mosquitto_topic: str

    postgres_host: str = "database"
    postgres_user: str
    postgres_password: str
    postgres_db: str

    @property
    def sqlalchemy_url(self):
        host = self.postgres_host
        username = self.postgres_user
        password = self.postgres_password
        database_name = self.postgres_db
        return f"postgresql+psycopg2://{username}:{password}@{host}/{database_name}"


SETTINGS = Settings()
