from .models import Request
from datetime import datetime


class StoreRequest(object):
    def process_request(self, request):
        path = request.get_full_path()
        if request.is_ajax() or path[0:8] == '/static/':
            return None

        r = Request(link=path, time=datetime.now())
        r.save()
