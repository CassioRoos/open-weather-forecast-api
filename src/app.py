import asyncio
import socket
import logging
from tornado.platform import asyncio as tornado_asyncio

from configurations import config
from controllers import WeatherConditionApplication

hostname = socket.gethostname()
IP = socket.gethostbyname(hostname)

logging.basicConfig(level=logging.getLevelName(config.APP_CONF_LOG_LEVEL))

if __name__ == "__main__":
    tornado_asyncio.AsyncIOMainLoop().install()
    """ Configurações passadas para a base do handler """
    classes = {}
    app = WeatherConditionApplication(classes)
    porta = config.APP_PORT
    app.listen(porta)
    logging.info(f"Running on http://{IP}:{porta}. Press CTRL + C to stop.")
    loop = asyncio.get_event_loop()
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop = loop.close()
