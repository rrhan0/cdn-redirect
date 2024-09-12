from datetime import datetime, timezone
from pymongo import MongoClient
from flask import Flask
import gridfs
import os

from lib.controller import generate_snapshot, get_snapshot_url, get_page

start_time = datetime.now()

app = Flask(__name__)

# db_client = MongoClient(host=os.environ.get("DB_HOST", "localhost"),
#                         port=int(os.environ.get("DB_PORT", 27017)),
#                         username=os.environ.get("DB_USER", None),
#                         password=os.environ.get("DB_PASSWORD", None))
db_client = MongoClient(host=os.environ.get("DB_HOST", "localhost"),
                        port=int(os.environ.get("DB_PORT", 27017)))
db = db_client.pages
fs = gridfs.GridFS(db)


@app.route('/archive/<path:url>', methods=['GET'])
def list_snapshots(url):
    return get_snapshot_url(url, fs)


@app.route('/archive/<path:url>', methods=['POST'])
def create_snapshot(url):
    time_now = datetime.now(timezone.utc)
    timestamp = int(time_now.strftime("%Y%m%d%H%M%S"))
    return generate_snapshot(timestamp, url, fs)


@app.route('/archive/<path:url>/<int:timestamp>', methods=['POST'])
def get_snapshot(url, timestamp):
    return get_page(timestamp, url, fs)


@app.route("/status", methods=["GET"])
def status():
    end_time = datetime.now()
    duration = end_time - start_time

    days = duration.days
    seconds = duration.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    body = {
        "uptime": f"{days} days, {hours} hours, {minutes} minutes, {seconds}, seconds",
        "date": f"{datetime.utcnow().isoformat()}"
    }

    return body


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=8080, threaded=True)
