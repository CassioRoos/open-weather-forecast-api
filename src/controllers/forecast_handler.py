import json
import logging
from http import HTTPStatus

from tornado_swirl import schema

from commons.exceptions import RequestIdAlreadyExists, RequestIdNotFound, ParameterNotFound
from controllers.base_handler import BaseHandler
from services.forecast_service import ForecastService

service = ForecastService()


class ForecastHandler(BaseHandler):
    async def post(self):
        """Request to open wether the forecast of a predefined list of cities

        Request to open wether the forecast of a predefined list of cities

        Request Body:
            request_id (string) -- Unique identifier sent via request

        Returns:
            weather (SimpleResponse) -- Successful operation (HTTP 200 Ok)

        Error Responses:
            500 (ErrorResponse) -- Internal Server Error
            401 (SimpleResponse) -- Object Already Exists

        Tags:
            Forecast
        """

        try:
            request_id = (await self.validate_body(json.loads(self.request.body)))["request_id"]
            response = await service.get_all_wether_conditions_from_list(request_id)
        except RequestIdAlreadyExists:
            self.set_status(HTTPStatus.UNAUTHORIZED)
            response = {"message": f"A record already exists for this id : {request_id}"}
        except ParameterNotFound:
            self.set_status(HTTPStatus.UNAUTHORIZED)
            response = {"message": f"The parameter request_id was not informed"}
        except Exception as e:
            self.set_status(HTTPStatus.INTERNAL_SERVER_ERROR)
            logging.error(e, stack_info=True, exc_info=True)
            response = {"message": "An error has occurred",
                        "error": format(e)}
        else:
            self.set_status(HTTPStatus.OK)
        finally:
            self.write(response)
            await self.finish()

    async def validate_body(self, body):
        request_id = body.get("request_id", None)
        if not request_id:
            raise ParameterNotFound()
        return body


class ForecastIdHandler(BaseHandler):
    async def get(self, requestid):
        """Request to open wether the forecast of a predefined list of cities

        Request to open wether the forecast of a predefined list of cities

        Path params:
            request_id (string) -- Unique identifier sent via request

        200 Response:
           weather (WeatherResponse) -- Successful operation (HTTP 200 Ok)

        Error Responses:
            500 (ErrorResponse) -- Internal Server Error
            404 (SimpleResponse) -- Not Found

        Tags:
            Forecast
        """
        try:
            response = await service.get_progress_percentage(request_id=int(requestid))
        except RequestIdNotFound:
            self.set_status(HTTPStatus.NOT_FOUND)
            response = {"message": f"No result was found for the id : {requestid}"}
        except Exception as e:
            self.set_status(HTTPStatus.INTERNAL_SERVER_ERROR)
            logging.error(e, stack_info=True, exc_info=True)
            response = {"message": "An error has occurred",
                        "error": format(e)}
        else:
            self.set_status(HTTPStatus.OK)
        finally:
            self.write(response)
            await self.finish()


@schema
class WeatherResponse(object):
    """ Weather response with the list of cities

        Properties:
            request_id (string) -- Unique identifier sent via request
            request_time (string) -- Date when the request occurred (Format dd/mm/yyyy hh:mm:ss)
            message (string) -- A message with the percentage of cities with the corresponded forecas
            forecast ([Forecast]) -- List of objects with the weather forecast
    """
    pass


@schema
class Forecast(object):
    """ Weather forecast for the city

    Properties:
        cityid (int) -- City id.
        temperature (int) -- Temperature in celsius.
        humidity (int) -- Humidity.
    """
    pass


@schema
class ErrorResponse(object):
    """Error response object.

    Properties:
        message (string) -- Fixed message "An error has occurred".
        error (string) -- Error description.
    """
    pass


@schema
class SimpleResponse(object):
    """Error response object.

    Properties:
        message (string) -- Message.
    """
    pass
