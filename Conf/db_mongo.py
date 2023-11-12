import configparser
import pathlib
from mongoengine import connect

file_config = pathlib.Path(__file__).parent.parent.joinpath('config.ini')
config = configparser.ConfigParser()
config.read(file_config)

username = config.get('DB', 'USER')
password = config.get('DB', 'PASSWORD')
db_name = config.get('DB', 'DB_NAME')
domain = config.get('DB', 'DOMAIN')
retry_writes = config.get('DB', 'RETRY_WRITES')
ssl = config.get('DB', 'SSL')

URI = f"""mongodb+srv://{username}:{password}@{domain}/{db_name}?retryWrites=true&w=majority"""

connect(host=URI)