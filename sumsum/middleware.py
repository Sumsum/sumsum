from threading import local


_local = local()


def get_request():
    return _local.request


class RequestLocalMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _local.request = request
        response = self.get_response(request)
        del _local.request
        return response
