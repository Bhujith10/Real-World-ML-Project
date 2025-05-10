from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='services/trades/settings.env', env_file_encoding='utf-8'
    )

    product_ids: list[str] = [
        'BTC/USD',
        'BTC/EUR',
        'ETH/EUR',
        'ETH/USD',
        'SOL/USD',
        'SOL/EUR',
        'XRP/USD',
        'XRP/EUR',
    ]
    # The below two variables are not assigned values here
    # which means they should be present in the env file
    kafka_broker_address: str 
    kafka_topic_name: str


config = Settings()
