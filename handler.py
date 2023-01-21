import json

import http_resp
import base_handler


class EasyMorningHandler(base_handler.Handler):
    
    def __init__(self, light_manager):
        self.light_manager = light_manager      
    
    def get_response(self, request):
        
        if request.path == "/status":
            return self.get_status_response()
        else:
            return self.get_default_response()
    
    def get_status_response(self):
        status = self.light_manager.get_status()
        content = json.dumps(status)
        return http_resp.HttpResponse(
                status=200,
                headers={"Content-Type": "application/json"},
                content=content,
            )
    
    def get_default_response(self):
        return http_resp.HttpResponse(
                status=404,
                headers={},
                content=b"Could not find resource.",
            )
        
        
