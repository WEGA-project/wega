from django.conf import settings


class Wega:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        request.wega_one_user = False
        
        if settings.WEGA_DEFAULT_PASSWORD and settings.WEGA_DEFAULT_USER:
            request.wega_one_user = True
        response = self.get_response(request)
        
        return response