
# set python path?
import os
import sys
sys.path.append(os.getcwd())

import json
import redis
import src.utils.errors
import src.databases.redisutil

# -------- loading secrets
# load .env file to environment
from dotenv import load_dotenv  # <--------------- Poetry does not support dotenv
load_dotenv()
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
#print(f'REDIS_PASSWORD={REDIS_PASSWORD}')


redis_connector = src.databases.redisutil.RedisConnector(
        host='localhost',
        port=6379,          #os.getenv('REDIS_PORT'),
        password=REDIS_PASSWORD,
)

with open('apikey_backup.json','r') as fp:
    data = json.load(fp)

try:
    pipe = redis_connector.connection.pipeline()
    for k,v in data.items():
        print(k, v)
        pipe.set(k, v)
    pipe.execute()
except:
    redis_connector.close()

redis_connector.close()
