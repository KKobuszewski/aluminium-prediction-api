
# set python path?
import os
import sys
sys.path.append(os.getcwd())

import redis
import argparse
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


parser = argparse.ArgumentParser()
parser.add_argument('-a', '--apikey')
parser.add_argument('-u', '--user', default='default_user')
args = parser.parse_args()

print(args)

try:
    redis_connector.connection.set(args.apikey, args.user)       # convention {apikey : user_type}
except:
    redis_connector.close() 
redis_connector.close()
