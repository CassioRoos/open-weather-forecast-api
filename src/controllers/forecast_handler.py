import json
import logging
from abc import ABC
from http import HTTPStatus

from tornado_swirl import schema

from commons.exceptions import RequestIdAlreadyExists, RequestIdNotFound, ParameterNotFound
from controllers.base_handler import BaseHandler
from services.forecast_service import ForecastService

service = ForecastService()


class ForecastIdHandler(BaseHandler):

    async def get(self, clientid):
        """Get the percentage of records requested

        Get the percentage of records requested

        Query params:
            request_id (string) -- Unique identifier sent via request

        200 Response:
           weather (WeatherResponseComplete) -- Successful operation (HTTP 200 Ok)

        Error Responses:
            500 (ErrorResponse) -- Internal Server Error
            404 (SimpleErrorResponse) -- Not Found

        Tags:
            Forecast
        """

        try:
            response = await service.get_progress_percentage(request_id=clientid)
        except RequestIdNotFound:
            self.set_status(HTTPStatus.NOT_FOUND)
            response = {"message": f"No result was found for the id : {clientid}"}
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


class ForecastHandler(BaseHandler):
    async def post(self):
        """Request to open wether the forecast of a predefined list of cities

        Request to open wether the forecast of a predefined list of cities

        Request Body:
            request_id (string) -- Unique identifier sent via request

        Returns:
            weather (WeatherResponse) -- Successful operation (HTTP 200 Ok)

        Error Responses:
            500 (ErrorResponse) -- Internal Server Error
            401 (SimpleErrorResponse) -- Object Already Exists

        Tags:
            Forecast
        """

        try:
            clientid = (await self.validate_body(json.loads(self.request.body)))["clientid"]
            response = await service.get_all_wether_conditions_from_list(clientid)
        except RequestIdAlreadyExists:
            self.set_status(HTTPStatus.UNAUTHORIZED)
            response = {"message": f"A record already exists for this id : {clientid}"}
        except ParameterNotFound:
            self.set_status(HTTPStatus.UNAUTHORIZED)
            response = {"message": f"The parameter clientid was not informed"}
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
        clientid = body.get("clientid", None)
        if not clientid:
            raise ParameterNotFound()
        return body


@schema
class WeatherResponse(object):
    """ Weather response with the list of cities

        Properties:
            request_id (string) -- Unique identifier sent via request
            request_time (string) -- Date when the request occurred (Format dd/mm/yyyy hh:mm:ss)
            forecast ([Forecast]) -- List of objects with the weather forecast
    """
    pass


@schema
class WeatherResponseComplete(object):
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
        message (string) -- Simple message.
    """
    pass
