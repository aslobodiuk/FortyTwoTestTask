from .models import Request
from datetime import datetime


class StoreRequest(object):
    def process_request(self, request):
        if request.is_ajax():
            return None

        r = Request(link=request.get_full_path(), time=datetime.now())
        r.save()
