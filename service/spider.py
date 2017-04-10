import json
import aiohttp
from collections import defaultdict
from http.cookies import SimpleCookie

grade_index_url = "http://122.204.187.6/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdmKey=N305005&sessionUserKey=%s"
link_index_url = "http://portal.ccnu.edu.cn/roamingAction.do?appId=XK"
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}

async def _get_grade(session, payload, ip, sid):
    grade_url = grade_index_url % sid
    link_url = link_index_url
    async with session.get(link_url, proxy=ip, timeout=4):
        async with session.post(grade_url, data=payload, proxy=ip) as resp:
            try:
                json_data = await resp.json()
                gradeList = []
                _gradeList = json_data.get('items')
                for _ in _gradeList:
                    gradeList.append({
                        'course'  : _.get('kcmc'),
                        'credit'  : _.get('xf'),
                        'grade'   : _.get('cj'),
                        'category': _.get('kclbmc'),
                        'type'    : _.get('kcgsmc'),
                        'jxb_id'  : _.get('jxb_id'),
                        'kcxzmc'  : _.get('kcxzmc')})
                return gradeList
            except json.decoder.JSONDecodeError:
                return [None]

async def get_grade(s, sid, ip, xnm, xqm):
    payload = {
        'xnm': xnm, 'xqm': xqm,
        '_search': 'false', 'nd': '1487928673156',
        'queryModel.showCount': 15, 'queryModel.currentPage': 1,
        'queryModel.sortName': "", 'queryModel.sortOrder': 'asc',
        'time': 0}
    s._unsafe = True # enabling cookie processing for IP addresses.
    async with aiohttp.ClientSession(cookie_jar=s, headers=headers) as session:
        try:
            rv = await _get_grade(session, payload, ip, sid)
            return rv
        except Exception:
            return [None] # faild...retry
