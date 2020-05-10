from tornado_swirl import schema


@schema
class Forecast(object):
    """ Weather forecast for the city

    Properties:
        cityid (int) -- City id
        temperature -- Temperature in celsius
        humidity -- Humidity
    """
    pass
