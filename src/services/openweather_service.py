import requests
from tornado.httputil import url_concat

from configurations import config


class OpenWeatherService:
    def get_forecast_for_city_id(self, city_id):
        query_params = {"appid": config.WEATHER_API_USER_KEY,
                        "units": config.WEATHER_API_UNITS,
                        "id": city_id}
        url = url_concat(config.WEATHER_API_BASE_URL, query_params)
        return self.exec_request(url)

    def exec_request(self, url):
        return requests.request("GET", url, timeout=config.WEATHER_API_DEFAULT_TIMEOUT)
