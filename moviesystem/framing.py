"""Allow this site to be embedded only by the owner's portfolio.

Replaces Django's X-Frame-Options (which can only say DENY or SAMEORIGIN) with a
Content-Security-Policy frame-ancestors allow-list, so vaibhavgawad.com can show a
live preview in an iframe while every other site is still blocked (clickjacking).
"""
from django.conf import settings


class FrameAncestorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        sources = getattr(settings, "FRAME_ANCESTORS", ["'self'"])
        self.header = "frame-ancestors " + " ".join(sources)

    def __call__(self, request):
        response = self.get_response(request)
        if "X-Frame-Options" in response:
            del response["X-Frame-Options"]
        response["Content-Security-Policy"] = self.header
        return response
