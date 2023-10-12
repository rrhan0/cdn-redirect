from datetime import datetime
import base64
import requests
import subprocess
from flask import Flask, jsonify, Response

VERSION = "1.0.0"

app = Flask(__name__)

webpage2html = "python webpage2html.py"


@app.route('/redirect/<path:url>', methods=['GET'])
def redirect_wrapper(url):
    if not (url.startswith('http://') or url.startswith('https://')):
        url = f'https://{url}'
    command = f"python  venv/lib/python3.11/site-packages/webpage2html.py -q {url}"

    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True, shell=True)
        return Response(output, content_type='text/html')
    except Exception as e:
        output = e.output
        return Response(output, content_type='text/html', status=500)



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
