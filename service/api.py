from aiohttp import web
from .decorator import require_info_login

api = web.Application()

# ====== async view handlers ======
@require_info_login()
async def api_index(request, s, sid):
    return web.json_response({})
# =================================

# ====== url --------- maps  ======
api.router.add_route('GET', '/info/login/', api_index, name='api_index')
# =================================
