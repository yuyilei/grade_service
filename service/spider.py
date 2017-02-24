import json
# import http.cookies.SimpleCookie as SimpleCookie
from collections import defaultdict
from http.cookies import SimpleCookie
import aiohttp

grade_index_url = "http://122.204.187.6/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdmKey=N305005&sessionUserKey=%s"
link_index_url = "http://portal.ccnu.edu.cn/roamingAction.do?appId=XK"
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}

async def get_grade(s, sid, xnm, xqm):
    grade_url = grade_index_url % sid
    link_url = link_index_url
    payload = {
        'xnm': xnm, 'xqm': xqm,
        '_search': 'false', 'nd': '1487928673156',
        'queryModel.showCount': 15, 'queryModel.currentPage': 1,
        'queryModel.sortName': "", 'queryModel.sortOrder': 'asc',
        'time': 0}
    s._unsafe = True # enabling cookie processing for IP addresses.
    async with aiohttp.ClientSession(cookie_jar=s, headers=headers) as session:
        # error handle
        async with session.get(link_url) as resp: # 302, Set-Cookie
            await resp.release() # release response
            async with session.post(grade_url, data=payload) as resp:
                try:
                    # print(await resp.text())
                    print('Success')
                    json_data = await resp.json() # may be return None
                except json.decoder.JSONDecodeError:
                    print('Failure')
                    return []
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
