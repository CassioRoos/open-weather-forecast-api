import json
import os
from http import HTTPStatus

from tornado.httpclient import HTTPResponse, HTTPRequest

TEST_PATH = os.path.dirname(__file__)
# MOCKS_PATH = os.path.join(TEST_PATH, "..", "resources")
MOCKS_PATH = os.path.join(TEST_PATH, "resources")


def file_from_resource(file_name, encoding=None):
    complete_file_name = os.path.join(MOCKS_PATH, file_name)
    with open(complete_file_name, encoding=encoding) as file:
        return json.loads(file.read())


def forecast_mock(file):
    body = file_from_resource(f"{file}.json")
    request = HTTPRequest(
        method='POST',
        body=json.dumps(body),
        url='about:blank')
    resp = HTTPResponse(request, HTTPStatus.OK, buffer=json.dumps({}))
    resp._body = json.dumps(body)
    resp.text = json.dumps(body)
    resp.status_code = HTTPStatus.OK
    return resp
