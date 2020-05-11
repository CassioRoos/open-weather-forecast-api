import json
import logging
import time
from http import HTTPStatus

from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.httputil import url_concat

from commons.mongo_connection import new_string_object_id
from commons.utils import get_cities
from configurations import config
from repository.forecast_repository import ForecastRepository


class OpenWeatherService:
    def __init__(self):
        self.repository = ForecastRepository()
        self.request_count = 0
        self.start_time = None
        self.header = {
            "content-type": "application/json",
            "accept": "application/json",
            "accept-encoding": "gzip, deflate",
            "accept-language": "en-US,en;q=0.8",
            "user-agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/64.0.3282.186 Safari/537.36")}

    async def get_forecast_for_city_id(self, city_id):
        query_params = {"appid": config.WEATHER_API_USER_KEY,
                        "units": config.WEATHER_API_UNITS,
                        "id": city_id}
        url = url_concat(config.WEATHER_API_BASE_URL, query_params)
        return await self.exec_request(url)

    async def exec_request(self, url):
        http_client = AsyncHTTPClient()
        request = HTTPRequest(
            headers=self.header,
            method="GET",
            body=None,
            url=url,
            request_timeout=config.WEATHER_API_DEFAULT_TIMEOUT)
        return await http_client.fetch(request, raise_error=False)

    async def get_forecast_to_all_cities(self, request_id):
        time.clock()
        request_time = time.time()
        self.start_time = request_time
        for city_id in get_cities():
            await self.process_request(city_id, request_id, request_time)
            # response = await self.get_forecast_for_city_id(city_id)
            # await self.parse_and_store_reponse(city_id, response, request_id, request_time)

    async def process_request(self, city_id, request_id, request_time):
        elapsed = time.time() - self.start_time
        if self.request_count == 60 and 60 > elapsed:
            time.sleep(60 - elapsed)
            self.request_count = 0
            self.start_time = time.time()

        self.start_time = time.time()
        response = await self.get_forecast_for_city_id(city_id)
        await self.parse_and_store_reponse(city_id, response, request_id, request_time)
        self.request_count += 1

    async def parse_and_store_reponse(self, city_id, response, request_id, request_time):
        if response.code != HTTPStatus.OK:
            logging.error(
                f"Error while getting data from OpenApi. \n "
                f"error code: {response.code} \n "
                f"error message: {response.body}")
            return
        forecast = json.loads(response.body)["list"][0]["main"]

        data = {"_id": new_string_object_id(),
                "request_id": request_id,
                "request_time": request_time,
                "cityid": city_id,
                "temp": forecast["temp"],
                "humidity": forecast["humidity"]}
        logging.debug(data)
        self.repository.insert(data)
        logging.debug(f"{city_id} ---> {response.code} ")
