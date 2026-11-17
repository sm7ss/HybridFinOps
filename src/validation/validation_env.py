from pydantic_settings import BaseSettings, SettingsConfigDict

class telegramValidation(BaseSettings): 
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_CHAT_ID: int

class awsValidation(BaseSettings):
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str

class validation_env(BaseSettings): 
    telegram: telegramValidation= telegramValidation()
    aws: awsValidation= awsValidation()
    
    model_config = SettingsConfigDict(
        env_file='.env', 
        env_file_encoding='utf-8', 
        extra='ignore'
    )





