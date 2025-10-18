from django.http import HttpResponsePermanentRedirect

class WWWRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split(':')[0]
        
        # Check if it's the non-www version
        if host == 'mastergiver.com':
            # Build the new URL with www
            protocol = 'https' if request.is_secure() else 'http'
            new_url = f"{protocol}://www.mastergiver.com{request.get_full_path()}"
            return HttpResponsePermanentRedirect(new_url)
        
        return self.get_response(request)