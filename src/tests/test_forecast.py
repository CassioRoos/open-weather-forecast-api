import json
from http import HTTPStatus
from time import sleep
from unittest import mock

from pymongo import MongoClient

from configurations import uris, config
from tests import TestWeatherConditionApplication
from tests.utils import forecast_mock


class TestFocastHandler(TestWeatherConditionApplication):
    def setUp(self):
        config.WEATHER_API_BASE_URL = "ALL DATA WILL BE MOCKED"
        self.conn = MongoClient(config.DB_HOST, config.DB_PORT)
        self.dropCollection()
        self.url = uris.URL_CONTEXT_FORECAST
        TestWeatherConditionApplication.setUp(self)

    def dropCollection(self):
        self.conn.drop_database(config.DB_NAME)

    def test_get_not_found(self):
        url = f"{self.url}/113"
        response = self.fetch(url, method="GET")
        self.assertEqual(HTTPStatus.NOT_FOUND, response.code)
        body_response = b'{"message": "No result was found for the id : 113"}'
        self.assertEqual(body_response, response.body)

    @mock.patch("services.openweather_service.OpenWeatherService.exec_request")
    def test_post_success(self, mock):
        request_id = 123
        self.insert_forecast(mock, request_id)

    @mock.patch("services.openweather_service.OpenWeatherService.exec_request")
    def test_unique_id_per_request(self, mock):
        request_id = 313
        self.insert_forecast(mock, request_id)
        sleep(1.5)
        body = json.dumps({"request_id": request_id})
        response = self.fetch(self.url, method="POST", body=body)
        self.assertEqual(HTTPStatus.UNAUTHORIZED, response.code)
        response_body = {"message": f"A record already exists for this id : {request_id}"}
        self.assertEqual(json.loads(response.body), response_body)

    def insert_forecast(self, mock, request_id):
        mock.side_effect = [forecast_mock(524901),
                            forecast_mock(3439525),
                            forecast_mock(3439781),
                            forecast_mock(3440645),
                            forecast_mock(3442098)]
        body = json.dumps({"request_id": request_id})
        response = self.fetch(self.url, method="POST", body=body)
        self.assertEqual(HTTPStatus.OK, response.code)
        response_body = json.loads(response.body)
        self.assertEqual(response_body["message"], "Your request will be processed in background")

    def test_post_with_no_body(self):
        response = self.fetch(self.url, method="POST", body=json.dumps(dict()))
        self.assertEqual(HTTPStatus.UNAUTHORIZED, response.code)
        self.assertEqual(json.loads(response.body)["message"], "The parameter request_id was not informed")

    @mock.patch("services.openweather_service.OpenWeatherService.exec_request")
    def test_get_progress_request(self, mock):
        request_id = 513
        self.insert_forecast(mock, request_id)
        sleep(1.5)
        url = f"{self.url}/{request_id}"
        response = self.fetch(url, method="GET")
        self.assertEqual(HTTPStatus.OK, response.code)
        response_body = json.loads(response.body)
        self.assertEqual(response_body["request_id"], request_id)
        self.assertEqual(len(response_body["forecast"]), 5)
        self.assertEqual(response_body["message"], "The percentage of progress is 100.0%")
