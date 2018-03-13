from aiohttp import web
from aiohttp.web import Response
from .spider import get_grade
from .szkc_spider import pre_get_szkc_grade
from .decorator import require_info_login


api = web.Application()

# ====== async view handlers ======
@require_info_login
async def grade_all_api(request, s, sid, ip):
    query_string = request.rel_url.query_string
    if query_string:
        keys = []; vals = []
        for _ in query_string.split('&'):
            keys.append(_.split('=')[0])
            vals.append(_.split('=')[1])
        args = dict(zip(keys, vals))
        xnm = args.get('xnm'); xqm = args.get('xqm')
        gradeList = await get_grade(s, sid, ip, xnm, xqm)
        szkcList = await pre_get_szkc_grade(sid,xnm,xqm)
        if gradeList :
            gradeList.extend(szkcList)
            return web.json_response(gradeList)
        else:
            return Response(body=b'', content_type='application/json', status=403)
# =================================

# ====== url --------- maps  ======
api.router.add_route('GET', '/grade/', grade_all_api, name='grade_all_api')
# =================================
