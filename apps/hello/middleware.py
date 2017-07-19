from .models import Request


class StoreRequest(object):
    def process_request(self, request):
        path = request.get_full_path()
        if request.is_ajax() or path[0:9] == '/uploads/':
                return None

        Request.objects.create(link=path)
