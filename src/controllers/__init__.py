from tornado_swirl import Application, restapi, describe, add_global_tag

from configurations import config, uris
from controllers.forecast_handler import ForecastHandler, ForecastIdHandler


class WeatherConditionApplication(Application):
    def __init__(self, classes):
        self.url_handlers = list()

        self.register_route(uris.VURI_FORECAST_request_id, ForecastIdHandler)
        self.register_route(uris.VURI_FORECAST, ForecastHandler)
        settings = {
            "debug": config.APP_CONF_DEBUG,
            "use_full_url": config.APP_CONF_FULL_URL,
            **classes,
            "compress_response": config.APP_CONF_COMPRESS_RESPONSE
        }
        add_global_tag('Forecast', 'URIs responsible for')
        describe('Weather forecast by CRoos', 'API that consumes open wethear forecast')
        super().__init__(self.url_handlers, **settings)

    def register_route(self, path, hanlder):
        restapi(path)(hanlder)
        self.url_handlers.append((path, hanlder))
