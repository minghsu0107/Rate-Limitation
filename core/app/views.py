from app.rateLimit import rateLimitMiddleware
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
@rateLimitMiddleware(**settings.REQUEST_LIMITATION)
def DemoLimitRateView(request, *args, **kwargs):
	return Response({'content': 'success!'})