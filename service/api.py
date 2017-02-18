from aiohttp import web

api = web.Application()

# ====== async view handlers ======
async def api_index(request):
    data = {'login': 'api'}
    return web.json_response(data)
# =================================

# ====== url --------- maps  ======
api.router.add_route('GET', '/', api_index, name='api_index')
# =================================
