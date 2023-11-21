from datetime import datetime
# from pymongo import MongoClient
import subprocess
import os
from flask import Flask, jsonify, Response

VERSION = "1.0.0"

app = Flask(__name__)

# db_client = MongoClient("localhost", 27017)


@app.route('/redirect/<path:url>', methods=['GET'])
def redirect_wrapper(url):
    if not (url.startswith('http://') or url.startswith('https://')):
        url = f'https://{url}'
    command = f'webpage2html -q {url}'

    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True, shell=True)
        return Response(output, content_type='text/html')
    except subprocess.CalledProcessError as e:
        print(e)
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
