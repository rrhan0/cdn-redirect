import socket
from datetime import datetime, timezone

from pymongo import DESCENDING, MongoClient
from gridfs import GridFS
from flask import Response
from webpage2html import generate

ip_address = socket.gethostbyname(socket.gethostname())


def generate_snapshot(timestamp: int, url: str, fs: GridFS):
    if not fs.exists(url=url, timestamp=timestamp):
        try:
            output = generate(url, verbose=False, keep_script=True)
            fs.put(output.encode('utf-8'), url=url, timestamp=timestamp)
        except Exception as e:
            print(e)
            try:
                output = generate(url, verbose=False, keep_script=False)
                fs.put(output.encode('utf-8'), url=url, timestamp=timestamp)
            except Exception as e:
                print(e)


def get_snapshot_url(url: str, fs: GridFS):
    urls = []

    for record in fs.find(url=url).sort('timestamp', DESCENDING):
        urls.append(f'{ip_address}/archive/{url}/{record.get("timestamp").strftime("%Y%m%d%H%M%S")}')
    return {
        'urls': urls
    }


def get_page(timestamp: int, url: str, fs: GridFS):
    record = fs.find_one({'url': url, 'timestamp': timestamp})
    file = record.read().decode('utf-8')
    return Response(file, content_type='text/html')