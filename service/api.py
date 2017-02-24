from aiohttp import web
from aiohttp.web import Response
from .spider import get_grade
from .login_service.service.decorator import require_info_login

api = web.Application()

# ====== async view handlers ======
@require_info_login()
async def grade_all_api(request, s, sid):
    query_string = request.rel_url.query_string
    if query_string:
        keys = []; vals = []
        for _ in query_string.split('&'):
            keys.append(_.split('=')[0])
            vals.append(_.split('=')[1])
        args = dict(zip(keys, vals))
        xnm = args.get('xnm'); xqm = args.get('xqm')
        gradeList = await get_grade(s, sid, xnm, xqm)
        return web.json_response(gradeList)
    else: # 404: need query string
        return Response(body = b'{}',
        content_type = 'application/json', status = 404)
# =================================

# ====== url --------- maps  ======
api.router.add_route('GET', '/grade/search/', grade_all_api, name='grade_all_api')
# =================================
