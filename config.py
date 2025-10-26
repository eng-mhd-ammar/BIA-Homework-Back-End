import os
import secrets

# Mysql Config
DB_USER = os.environ.get("SECRET_KEY", "root")
DB_PASSWORD = os.environ.get("SECRET_KEY", "062003")
DB_HOST = os.environ.get("SECRET_KEY", "localhost")
DB_PORT = os.environ.get("SECRET_KEY", "3306")
DB_NAME = os.environ.get("SECRET_KEY", "BIA")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

SECRET_KEY = os.environ.get("SECRET_KEY", secrets.token_hex(32))
