

class FirstMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        print(request.build_absolute_uri())
        response = self._get_response(request)
        return response


class SecondMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        print('second MiddleWare, before')
        response = self._get_response(request)
        print('second MiddleWare, after')
        return response