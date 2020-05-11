import logging

from bson import ObjectId
from pymongo import monitoring, MongoClient

from configurations import config

mongo_client = MongoClient(host=config.DB_HOST, port=config.DB_PORT)[config.DB_NAME][config.DB_COLLECTION]


class CommandLogger(monitoring.CommandListener):
    def started(self, event):
        logging.debug("Command {0.command_name} with request id "
                      "{0.request_id} started on server "
                      "{0.connection_id} database {0.database_name}".format(event))

    def succeeded(self, event):
        database = event.reply.get('cursor', {'ns': None}).get('ns')
        logging.debug("Command {0.command_name} with request id "
                      "{0.request_id} on server {0.connection_id}"
                      "succeeded in {0.duration_micros} database {1} "
                      "microseconds".format(event, database))

    def failed(self, event):
        database = event.reply.get('cursor', {'ns': None}).get('ns')
        logging.debug("Command {0.command_name} with request id "
                      "{0.request_id} on server {0.connection_id} database {1} "
                      "failed in {0.duration_micros} "
                      "microseconds".format(event, database))


monitoring.register(CommandLogger())


def new_string_object_id():
    return str(ObjectId())
