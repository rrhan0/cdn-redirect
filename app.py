from datetime import datetime

from flask import Flask, redirect, jsonify

VERSION = "1.0.0"

app = Flask(__name__)


@app.route('/redirect/<path:url>', methods=['GET'])
def redirect_wrapper(url):
    if url.startswith('http://') or url.startswith('https://'):
        return redirect(url)
    else:
        return redirect(f'https://{url}')


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
