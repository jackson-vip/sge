import os
from django.middleware.security import SecurityMiddleware

class CustomSecurityMiddleware(SecurityMiddleware):
    def process_response(self, request, response):
        # Aplica o cabeçalho apenas em desenvolvimento
        if os.getenv('DJANGO_ENV', 'development') == 'development' and request.get_host().startswith('localhost'):
            response['Cross-Origin-Opener-Policy'] = 'same-origin'
        return super().process_response(request, response)