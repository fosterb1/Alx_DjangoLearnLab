# LibraryProject/middleware.py
"""
Content Security Policy (CSP) Middleware
Implements CSP headers to prevent XSS attacks by restricting content sources.
"""

class CSPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Content Security Policy header
        # Restricts where resources can be loaded from to prevent XSS
        csp_policy = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; "
            "style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; "
            "img-src 'self' data: https:; "
            "font-src 'self' https://cdnjs.cloudflare.com; "
            "connect-src 'self'; "
            "object-src 'none'; "
            "base-uri 'self';"
        )
        
        response['Content-Security-Policy'] = csp_policy
        return response