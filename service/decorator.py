import functools
import json
import base64
from aiohttp.web import Response
from .spider import info_login

def require_info_login():
    def decorator(f):
        @functools.wraps(f)
        async def decorated_function(request, *args, **kwargs):
            authorized = False
            headers = request.headers # .keys()
            req_headers = dict(headers)

            basic_auth_header = req_headers.get('Authorization')
            if basic_auth_header:
                auth_header = basic_auth_header[6:]
                uid, pwd = base64.b64decode(auth_header).decode().split(':')
                # session, sid
                s, sid = await info_login(uid, pwd)
                if s is None:
                    return Response(body = b'{}',
                    content_type = 'application/json', status = 403)
                else: authorized = True

            if authorized:
                response = await f(request, s, sid, *args, **kwargs)
                return response
            else:
                return Response(body = b'{}',
                content_type = 'application/json', status = 401)
        return decorated_function
    return decorator
