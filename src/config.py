import os

env = os.environ.get("ENV", "dev")

if env == "dev":
	from dotenv import load_dotenv

	load_dotenv(".env.local")


db_connection_str = os.environ.get("CONNECTION_STR")
