from pymongo import MongoClient
from tornado.testing import AsyncHTTPTestCase

from configurations import config
from controllers import WeatherConditionApplication


class TestWeatherConditionApplication(AsyncHTTPTestCase):
    def get_app(self):
        app = WeatherConditionApplication(dict())
        return app

    def setUp(self):
        config.DB_NAME = "weather_test"
        AsyncHTTPTestCase.setUp(self)

    def dropCollection(self):
        self.conn.drop_database(config.DB_NAME)
