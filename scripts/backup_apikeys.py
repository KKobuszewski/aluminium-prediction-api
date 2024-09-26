
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

try:
    data = {key.decode('utf-8') : redis_connector.connection.get(key).decode('utf-8') for key in redis_connector.connection.keys()}
    with open('apikey_backup.json','w') as fp:
        json.dump(data, fp)
except:
    print('# Backup of apikeys FAILED.')
    redis_connector.close()

print('# Backup of apikeys SUCCEDED.')
redis_connector.close()

