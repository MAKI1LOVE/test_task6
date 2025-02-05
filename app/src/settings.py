from pydantic_settings import BaseSettings


class RabbitSettings(BaseSettings):
    RABBIT_USER: str
    RABBIT_PASS: str
    RABBIT_QUEUE: str
    RABBIT_HOST: str

    @property
    def RABBIT_URL(self):
        return f"amqp://{self.RABBIT_USER}:{self.RABBIT_PASS}@{self.RABBIT_HOST}/"


class Settings(BaseSettings):
    rabbit_settings: RabbitSettings = RabbitSettings()


app_settings = Settings()
