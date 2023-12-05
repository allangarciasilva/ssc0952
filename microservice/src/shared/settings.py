from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_file=".env")
    debug: bool = True

    api_secret_key: str

    mosquitto_host: str = "broker"
    mosquitto_port: int = 1883
    mosquitto_user: str
    mosquitto_password: str

    postgres_host: str = "database"
    postgres_port: int = 5432
    postgres_user: str
    postgres_password: str
    postgres_db: str

    kafka_host: str
    kafka_port: int

    @property
    def sqlalchemy_url(self):
        host = self.postgres_host
        port = self.postgres_port
        username = self.postgres_user
        password = self.postgres_password
        database_name = self.postgres_db
        return f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database_name}"

    @property
    def kafka_server(self):
        return f"{self.kafka_host}:{self.kafka_port}"

    @classmethod
    def create(cls):
        settings = Settings()
        if settings.mosquitto_host == "broker":
            settings.mosquitto_port = 1883
        if settings.postgres_host == "database":
            settings.postgres_port = 5432
        return settings


SETTINGS = Settings.create()
