import json

import http_resp, http_req
import base_handler


class EasyMorningHandler(base_handler.Handler):
    
    def __init__(self, light_manager):
        self.light_manager = light_manager      
    
    def get_response(self, request):
        
        if request.method == "GET":
            if request.path == "/status":
                return self.get_status_response()
        elif request.method == "POST":
            if request.path.startswith("/now"):
                return self.set_now(request.path)
            elif request.path.startswith("/fade"):
                return self.set_fade(request.path)
            elif request.path.startswith("/timer"):
                return self.set_timer(request.path)
        
        return self.get_404_response()
    
    def get_status_response(self):
        status = self.light_manager.get_status()
        return self.get_json_response(status)
        
    def set_now(self, path):
        path, args, fragment = http_req.parse_path(path)
        level = float(args["level"])
        self.light_manager.constant(level)
        return self.get_json_response({"success": True})
    
    def set_fade(self, path):
        path, args, fragment = http_req.parse_path(path)
        level = float(args["level"])
        period = float(args["seconds"])
        self.light_manager.fade(period, level)
        return self.get_json_response({"success": True})
    
    def set_timer(self, path):
        path, args, fragment = http_req.parse_path(path)
        level = float(args["level"])
        period = float(args["seconds"])
        self.light_manager.timer(period, level)
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
        
        
