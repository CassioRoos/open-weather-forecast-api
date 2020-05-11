from tornado import web


class BaseHandler(web.RequestHandler):
    def set_default_headers(self):
        self.add_header("Access-Control-Allow-Origin", "*")
        self.add_header("Content-Type", "application/json")
