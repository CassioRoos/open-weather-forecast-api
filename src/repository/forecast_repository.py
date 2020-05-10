from commons.mongo_connection import mongo_client


class ForecastRepository():
    def __init__(self):
        self.db = mongo_client

    def find_by_request_id(self, request_id):
        return self.db.find({"request_id": request_id})

    def insert(self, data):
        mongo_client.insert_one(data)
