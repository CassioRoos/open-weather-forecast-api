URL_BASE = r"/api"

URL_CONTEXT_FORECAST = "/forecast"

URL_REGEX_request_id = fr"/(?P<requestid>\w+)"

VURI_FORECAST_request_id = f"{URL_CONTEXT_FORECAST}{URL_REGEX_request_id}"
VURI_FORECAST = f"{URL_CONTEXT_FORECAST}"
