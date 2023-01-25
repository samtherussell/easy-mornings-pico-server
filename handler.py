import json

import http_resp
import base_handler


class EasyMorningHandler(base_handler.Handler):
    def __init__(self, light_manager):
        self.light_manager = light_manager

    def get_response(self, request):

        if request.method == "GET":
            if request.path.startswith("/status"):
                return self.get_status_response()
            elif request.path == "/alarm":
                return self.get_alarms()
        elif request.method == "POST":
            if request.path == "/now":
                return self.now(request)
            elif request.path == "/fade":
                return self.fade(request)
            elif request.path == "/timer":
                return self.timer(request)
            elif request.path == "/rave":
                return self.rave(request)
            elif request.path == "/alarm":
                if "index" in request.args:
                    return self.update_alarm(request)
                else:
                    return self.add_alarm(request)
        elif request.method == "DELETE":
            if request.path == "/alarm":
                return self.delete_alarm(request)

        return self.get_404_response()

    def get_status_response(self):
        status = self.light_manager.get_status()
        return self.get_json_response(status)

    def get_alarms(self):
        alarms = self.light_manager.alarms.get_as_dicts()
        return self.get_json_response(alarms)

    def add_alarm(self, req):
        data = json.loads(req.content)
        self.light_manager.alarms.add_from_dict(data)
        return self.get_json_response({"success": True})

    def delete_alarm(self, req):
        index = int(req.args["index"])
        del self.light_manager.alarms[index]
        return self.get_json_response({"success": True})

    def update_alarm(self, req):
        index = int(req.args["index"])
        data = json.loads(req.content)
        self.light_manager.alarms.update_from_dict(index, data)
        return self.get_json_response({"success": True})

    def now(self, req):
        level = float(req.args["level"])
        self.light_manager.constant(level)
        return self.get_json_response({"success": True})

    def fade(self, req):
        level = float(req.args["level"])
        seconds = float(req.args["seconds"])
        self.light_manager.fade(seconds, level)
        return self.get_json_response({"success": True})

    def timer(self, req):
        level = float(req.args["level"])
        seconds = float(req.args["seconds"])
        self.light_manager.timer(seconds, level)
        return self.get_json_response({"success": True})

    def rave(self, path):
        self.light_manager.rave()
        return self.get_json_response({"success": True})

    def get_json_response(self, data):
        content = json.dumps(data)
        return http_resp.HttpResponse(
            status=200,
            headers={"Content-Type": "application/json"},
            content=content,
        )

    def get_404_response(self):
        return http_resp.HttpResponse(
            status=404,
            headers={},
            content=b"Could not find resource.",
        )

    def get_500_response(self, msg):
        return http_resp.HttpResponse(
            status=404,
            headers={},
            content=msg.encode(),
        )
