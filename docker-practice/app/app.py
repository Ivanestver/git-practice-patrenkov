from flask import Flask, render_template, redirect, url_for
import redis
import os

VALUE_KEY = 'value'
DEFAULT_APP_ENV_VALUE = 'dev'
REDIS_HOST_KEY = 'REDIS_HOST'
REDIS_PORT_KEY = 'REDIS_PORT'

r = None

value_global = 0 # for test purposes only

app = Flask(__name__)

def get_app_env():
    return os.getenv('APP_ENV', DEFAULT_APP_ENV_VALUE)

def is_redis():
    return get_app_env() == DEFAULT_APP_ENV_VALUE

@app.route('/')
def hello_world():
    value_to_send = 0
    storage_used = ""
    if is_redis():
        value = int(r.get(VALUE_KEY))
        value += 1
        r.set(VALUE_KEY, str(value))
        value_to_send = value
        storage_used = "redis"
    else:
        global value_global
        value_global += 1
        value_to_send = value_global
        storage_used = "memory"
    return render_template('index.html', h1 = value_to_send, storage = storage_used, app_env = get_app_env())

if __name__ == '__main__':
    if is_redis():
        r = redis.Redis(
                host=os.getenv(REDIS_HOST_KEY, "localhost"), 
                port=int(os.getenv(REDIS_PORT_KEY, "6379")), 
                db=0, decode_responses=True
        )
        if not r.exists(VALUE_KEY):
            r.set(VALUE_KEY, '0')
    app.run(host='0.0.0.0', port=5000, debug=True)
