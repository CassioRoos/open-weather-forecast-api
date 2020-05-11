import logging

from commons.exceptions import RequestIdAlreadyExists, RequestIdNotFound
from commons.utils import format_date, future_call, get_cities
from repository.forecast_repository import ForecastRepository
from services.openweather_service import OpenWeatherService

logger = logging.getLogger(__name__)


class ForecastService:
    def __init__(self):
        self.repository = ForecastRepository()
        self.open_weather_service = OpenWeatherService()

    async def trow_exception_if_exists(self, request_id):
        if self.repository.find_by_request_id(request_id).count():
            raise RequestIdAlreadyExists

    async def get_all_wether_conditions_from_list(self, request_id):
        future_call(self.open_weather_service.get_forecast_to_all_cities, request_id)
        response = {"message": "Your request will be processed in background"}
        return response

    async def get_progress_percentage(self, request_id):
        results = self.repository.find_by_request_id(request_id)
        if results.count() == 0:
            raise RequestIdNotFound()

        json_message = await self.__mount_json_reponse(request_id, results)
        return json_message

    async def __mount_json_reponse(self, request_id, results=None):
        if not results:
            results = self.repository.find_by_request_id(request_id)
        data_list = list()
        json_data = dict()
        for doc in results:
            json_data = {"request_id": doc["request_id"],
                         "request_time": format_date("%d/%m/%Y %H:%M:%S", doc["request_time"])}
            data_list.append({"cityid": doc["cityid"],
                              "temperatue": doc["temp"],
                              "humidity": doc["humidity"]})
        json_data["forecast"] = data_list

        progress_percentage = (results.count() * 100) / len(get_cities())
        json_message = {"message": f"The percentage of progress is {round(progress_percentage, 2)}%"}
        json_message.update(json_data)
        return json_message
