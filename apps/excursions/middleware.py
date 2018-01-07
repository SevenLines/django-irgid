from modeltranslation import settings
from django.utils import translation


class LanguageMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_view(self, request, *args, **kwargs):
        if translation.LANGUAGE_SESSION_KEY in request.session:
            lang = request.session[translation.LANGUAGE_SESSION_KEY]
            if lang in settings.AVAILABLE_LANGUAGES:
                translation.activate(lang)

