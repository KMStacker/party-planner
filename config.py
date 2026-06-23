import os

secret_key = os.environ.get("SECRET_KEY", "key_for_local_use_1234")
database_file = os.environ.get("DATABASE_FILE", "database.db")
