from .models import Request


class StoreRequest(object):
    def process_request(self, request):
        path = request.get_full_path()
        path_con = path[0:8] == '/static/' or path[0:9] == '/uploads/'
        if request.is_ajax() or path_con:
                return None

        Request.objects.create(link=path)
