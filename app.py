from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient
from flask import Flask, jsonify, Response
import subprocess
import gridfs
import os

VERSION = "1.0.1"

app = Flask(__name__)

load_dotenv()
db_client = MongoClient(host=os.environ.get("DB_HOST", "localhost"),
                        port=int(os.environ.get("DB_PORT", 27017)),
                        username=os.environ.get("DB_USER"),
                        password=os.environ.get("DB_PASSWORD"))
db = db_client.pages
fs = gridfs.GridFS(db)


@app.route('/redirect/<path:url>', methods=['GET'])
def redirect_wrapper(url):
    if not (url.startswith('http://') or url.startswith('https://')):
        url = f'https://{url}'
    command = f'webpage2html -q {url}'

    if fs.exists(url):
        file = fs.get(url).read().decode('utf-8')
        return Response(file, content_type='text/html')

    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True, shell=True)
        fs.put(output.encode('utf-8'), _id=url)
        return Response(output, content_type='text/html')
    except subprocess.CalledProcessError as e:
        return {'msg': 'failed'}, 500


@app.route("/healthcheck", methods=["GET"])
def healthcheck_endpoint():
    data = {
        "msg": f"Running version {VERSION}",
        "date": f"{datetime.utcnow().isoformat()[0:19]}Z",
    }
    return jsonify(data)


def main():
    app.run(debug=True, host='0.0.0.0', port=8080, threaded=True)


if __name__ == "__main__":
    main()
