from decouple import config

# #################

APP_PORT = config("APP_PORT", default=5001, cast=int)
APP_HOST = config("APP_HOST", default="localhost", cast=str)

# #################

APP_CONF_LOG_LEVEL = config("APP_CONF_LOG_LEVEL", default="WARNING", cast=str)
APP_CONF_DEBUG = config("APP_CONF_DEBUG", default=True, cast=bool)
APP_CONF_FULL_URL = config("APP_CONF_FULL_URL", default=True, cast=bool)
APP_CONF_COMPRESS_RESPONSE = config("APP_CONF_COMPRESS_RESPONSE", default=True, cast=bool)

# #################

DB_HOST = config("DB_HOST", default="localhost", cast=str)
DB_NAME = config("DB_NAME", default="weather", cast=str)
DB_COLLECTION = config("DB_COLLECTION", default="forecast", cast=str)
DB_PORT = config("DB_PORT", default=27017, cast=int)

# ################

WEATHER_API_BASE_URL = config("WEATHER_API_BASE_URL", default="http://api.openweathermap.org/data/2.5/group?", cast=str)
# WEATHER_API_BASE_URL = config("WEATHER_API_BASE_URL", default="http://api.openweathermap.org/data/2.5/forecast?", cast=str)
WEATHER_API_DEFAULT_TIMEOUT = config("WEATHER_API_DEFAULT_TIMEOUT", default=360, cast=int)
WEATHER_API_USER_KEY = config("WEATHER_API_USER_KEY", default="70425e4429115cf6ec80c7e0af121cd4", cast=str)
WEATHER_API_UNITS = config("WEATHER_API_UNITS", default="metric", cast=str)
WEATHER_API_MAX_REQUESTS_PER_MINUTE = config("WEATHER_API_MAX_REQUESTS_PER_MINUTE", default=60, cast=int)


