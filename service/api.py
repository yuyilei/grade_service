from aiohttp import web
from .login_service.service.decorator import require_info_login

api = web.Application()

# ====== async view handlers ======
@require_info_login()
async def grade_all_api(request, s, sid):
    return web.json_response({})
# =================================

# ====== url --------- maps  ======
api.router.add_route('GET', '/grade/search/', grade_all_api, name='grade_all_api')
# =================================
