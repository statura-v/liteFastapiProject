from dotenv import load_dotenv
import os

load_dotenv()

DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_PORT = os.environ.get("DB_PORT")
DB_HOST = os.environ.get("DB_HOST")

required_vars = ["DB_NAME", "DB_USER", "DB_PASS", "DB_PORT", "DB_HOST"]
for var in required_vars:
    if not os.environ.get(var):
        raise ValueError(f"Environment variable {var} is not set")

class RunConfig:
    def __init__(self, host: str = "0.0.0.0", port: int = 8000) -> None:
        self.host: str = host
        self.port: int = port

class Settings:
    def __init__(self) -> None:
        self.run: RunConfig = RunConfig()

        self.db_name: str = DB_NAME
        self.db_user: str = DB_USER
        self.db_pass: str = DB_PASS
        self.db_port: str = DB_PORT
        self.db_host: str = DB_HOST

settings = Settings()
