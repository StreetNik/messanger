from django.http import HttpResponseRedirect
from django.urls import reverse


class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        excluded_paths = [reverse('login'), reverse('registration')]
        if request.path not in excluded_paths:
            if not request.user.is_authenticated:
                return HttpResponseRedirect(reverse('login'))
        response = self.get_response(request)
        return response
