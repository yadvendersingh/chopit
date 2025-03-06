# db_adapter.py
import os
from dotenv import load_dotenv

load_dotenv()
DB_TYPE = os.getenv("DB_TYPE", "sqlite")

if DB_TYPE == "sqlite":
    from backend.db_sqlite import get_records_from_table, get_url_by_short, insert_url, increment_clicks, get_counter
# Currently using sqlite for development purposes but project can be extended with other databases like MySQL, PostgreSQL, NoSQL etc. 
# Support for additional databases can be added here and the environment file can be configured accordingly.