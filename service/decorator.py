import json
import functools
import aiohttp
from aiohttp.web import Response

info_login_service = 'http://0.0.0.0:8080/api/info/login/'

def require_info_login(f):
    @functools.wraps(f)
    async def decorator(request, *args, **kwargs):
        headers = request.headers
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(info_login_service, timeout=4) as resp:
                try:
                    resp = await resp.json()
                except json.decoder.JSONDecodeError:
                    return Response(
                        body = b'{"error": "info login service error"}',
                        content_type = 'application/json',
                        status = 500)
        if resp != {}:
            sid = resp.get('sid')
            pwd = resp.get('pwd')
            cookies = resp.get('cookie')
            return await f(request, cookies, sid, pwd, None, *args, **kwargs)
        else:
            return Response(body = b'', content_type = 'application/json',
                status = 403)
    return decorator
