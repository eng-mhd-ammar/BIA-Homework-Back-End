import os
import secrets

# Mysql Config
DB_USER = "root"
DB_PASSWORD = "062003"
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "BIA"

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

SECRET_KEY = os.environ.get("SECRET_KEY", secrets.token_hex(32))
