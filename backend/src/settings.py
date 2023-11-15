from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    mosquitto_host: str = "broker"
    mosquitto_port: int = 1883
    mosquitto_user: str
    mosquitto_password: str

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

    @classmethod
    def create(cls):
        settings = Settings()
        if settings.mosquitto_host == "broker":
            settings.mosquitto_port = 1883
        return settings


SETTINGS = Settings.create()
