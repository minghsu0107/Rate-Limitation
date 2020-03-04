from django.conf import settings
import time
from functools import update_wrapper
from redis import StrictRedis
from rest_framework import status
from rest_framework.response import Response

redis = StrictRedis(**settings.REDIS_CONFIG)

class RateLimit(object):

    def __init__(self, key, limit, window, send_x_headers):
        self.key = key
        self.limit = limit
        self.window = window
        self.send_x_headers = send_x_headers

        val = redis.hgetall(self.key)
        if not val:
            self.reset_at = int(time.time()) + window
            self.current = 1
            redis.hmset(self.key, {'reset_at': self.reset_at, 'current': self.current})
            redis.expireat(self.key, self.reset_at)
        else:
            self.reset_at = int(val['reset_at'])
            self.current = int(val['current']) + 1
            redis.hmset(self.key, {'reset_at': self.reset_at, 'current': self.current})

    remaining = property(lambda x: x.limit - x.current)
    reset = property(lambda x: x.reset_at - int(time.time()))
    over_limit = property(lambda x: x.current > x.limit)

def get_client_ip(request):
    ip = request.META.get('X-Real-IP')
    if ip is None:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def rateLimitMiddleware(limit=1000, window=3600, send_x_headers=True, scope_func=get_client_ip,
              error_context=None):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            key = f'{request.path}{scope_func(request)}/'
            rlimit = RateLimit(key, limit, window, send_x_headers)

            if rlimit.over_limit:
                nonlocal error_context
                if error_context is None:
                    error_context = "API rate limit exceeded"
                return Response({'error': error_context}, status=status.HTTP_429_TOO_MANY_REQUESTS)
            
            response = func(request, *args, **kwargs)
            response['X-RateLimit-Remaining'] = str(rlimit.remaining)
            response['X-RateLimit-Limit'] = str(rlimit.limit)
            response['X-RateLimit-Reset'] = str(rlimit.reset)
            return response
        return update_wrapper(wrapper, func)
    return decorator
