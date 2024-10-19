import os
from dotenv import load_dotenv
from pathlib import Path
from ._factory import Database


load_dotenv(dotenv_path=Path(__file__).parent.parent / '.env')


dbDev = Database(
    'mysql',
    database=os.getenv("DATABASE"),
    user=os.getenv("USER"),
    password=os.getenv("PASSWORD"),
)
