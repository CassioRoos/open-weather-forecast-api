import json
import logging
import time

from commons.exceptions import RequestIdAlreadyExists, RequestIdNotFound
from commons.mongo_connection import NewStringObjectId
from commons.utils import format_date
from repository.forecast_repository import ForecastRepository
from services.openweather_service import OpenWeatherService

logger = logging.getLogger(__name__)


class ForecastService:
    def __init__(self):
        self.header = {
            "content-type": "application/json",
            "accept": "application/json",
            "accept-encoding": "gzip, deflate",
            "accept-language": "en-US,en;q=0.8",
            "user-agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/64.0.3282.186 Safari/537.36")}
        self.requests_executed = 0
        self.cities_list = self.__get_cities()
        self.repository = ForecastRepository()
        self.open_weather_service = OpenWeatherService()

    def __get_cities(self):
        return [3439525, 3439781, 3440645, 3442098, 3442778]
        # , 3443341, 3442233, 3440781, 3441572,
        # 3441575, 3443207, 3442546, 3441287, 3441242, 3441686, 3440639, 3441354, 3442057,
        # 3442585, 3442727, 3439705, 3441890, 3443411, 3440054, 3441684, 3440711, 3440714,
        # 3440696, 3441894, 3443173, 3441702, 3442007, 3441665, 3440963, 3443413, 3440033,
        # 3440034, 3440571, 3443025, 3441243, 3440789, 3442568, 3443737, 3440771, 3440777,
        # 3442597, 3442587, 3439749, 3441358, 3442980, 3442750, 3443352, 3442051, 3441442,
        # 3442398, 3442163, 3443533, 3440942, 3442720, 3441273, 3442071, 3442105, 3442683,
        # 3443030, 3441011, 3440925, 3440021, 3441292, 3480823, 3440379, 3442106, 3439696,
        # 3440063, 3442231, 3442926, 3442050, 3440698, 3480819, 3442450, 3442584, 3443632,
        # 3441122, 3441475, 3440791, 3480818, 3439780, 3443861, 3440780, 3442805, 7838849,
        # 3440581, 3440830, 3443756, 3443758, 3443013, 3439590, 3439598, 3439619, 3439622,
        # 3439652, 3439659, 3439661, 3439725, 3439748, 3439787, 3439831, 3439838, 3439902,
        # 3440055, 3440076, 3440394, 3440400, 3440541, 3440554, 3440577, 3440580, 3440596,
        # 3440653, 3440654, 3440684, 3440705, 3440747, 3440762, 3440879, 3440939, 3440985,
        # 3441074, 3441114, 3441377, 3441476, 3441481, 3441483, 3441577, 3441659, 3441674,
        # 3441803, 3441954, 3441988, 3442058, 3442138, 3442206, 3442221, 3442236, 3442238,
        # 3442299, 3442716, 3442766, 3442803, 3442939, 3443061, 3443183, 3443256, 3443280,
        # 3443289, 3443342, 3443356, 3443588, 3443631, 3443644, 3443697, 3443909, 3443928,
        # 3443952, 3480812, 3480820, 3480822, 3480825]

    async def trow_exception_if_exists(self, request_id):
        if self.repository.find_by_request_id(request_id).count():
            raise RequestIdAlreadyExists

    async def get_all_wether_conditions_from_list(self, request_id):
        await self.trow_exception_if_exists(request_id)
        request_time = time.time()
        self.requests_executed = 0

        for cityid in self.cities_list:
            self.sync_request(cityid, request_id, request_time)

        total_time = format_date("%M:%S:%f", time.time() - request_time)
        logger.info(f"Execution time {total_time} ")

        response = await self.__mount_json_reponse(request_id)
        response.pop("message")
        return response

    def sync_request(self, city_id, request_id, request_time):
        # self.wait_a_minute()
        self.requests_executed += 1

        request = self.open_weather_service.get_forecast_for_city_id(city_id)

        forecast = json.loads(request.text)["list"][0]["main"]

        data = {"_id": NewStringObjectId(),
                "request_id": request_id,
                "request_time": request_time,
                "cityid": city_id,
                "temp": forecast["temp"],
                "humidity": forecast["humidity"]}
        logging.info(data)
        self.repository.insert(data)
        logging.info(f"{city_id} ---> {request.status_code}")

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

        progress_percentage = (results.count() * 100) / len(self.cities_list)
        json_message = {"message": f"The percentage of progress is {round(progress_percentage, 2)}%"}
        json_message.update(json_data)
        return json_message
