from .models import Request


class StoreRequest(object):
    def process_request(self, request):
        path = request.get_full_path()
        order = 0
        if request.is_ajax():
            return None
        if path.startswith('/admin/'):
            order = 3
        elif path.startswith('/static/'):
            order = 2
        elif path.startswith('/edit/'):
            order = 1
        Request.objects.create(link=path, link_type=order)
