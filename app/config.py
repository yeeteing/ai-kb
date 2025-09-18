from pydantic_settings import BaseSettings

#his class is for app configuration, 
# and it will load values from the environment or .env file.
class Settings(BaseSettings): 
    DATABASE_URL: str
    LLM_PROVIDER: str = "openai"
    OPENAI_API_KEY: str | None = None
    TOP_K: int = 4
    SCORE_THRESHOLD: float = 0.15

    #change behavior of the model.
    class Config:
        #load values from a file called .env (in addition to environment variables).
        #So don’t have to do os.environ.get(...) everywhere
        env_file = ".env"

settings = Settings() #creates an object of Settings class
print(settings.DATABASE_URL)    # reads from env/.env
print(settings.TOP_K)           # default = 4 if not set

