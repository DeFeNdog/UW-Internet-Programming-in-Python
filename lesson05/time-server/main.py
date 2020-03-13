import os
import time
from flask import Flask

# https://arcane-woodland-55868.herokuapp.com/unix-timestamp/

os.environ['TZ'] = 'America/Los_Angeles'
time.tzset()
ct = time.time()
app = Flask(__name__)
timestamp = int(time.time())


@app.route('/unix-timestamp/')
def get_unix_timestamp():
    return str(timestamp)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)
