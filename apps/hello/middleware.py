from .models import Request


class StoreRequest(object):
    def process_request(self, request):
        path = request.get_full_path()
        if request.is_ajax() or path[0:9] == '/uploads/':
                return None
        order = 0
        if path[0:7] == '/admin/':
            order = 3
        elif path[0:8] == '/static/':
            order = 2
        elif path[0:6] == '/edit/':
            order = 1
        Request.objects.create(link=path, link_type=order)
