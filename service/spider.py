import json
import aiohttp

grade_index_url = "http://122.204.187.6/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdmKey=N305005&sessionUserKey=%s"
link_index_url = "http://portal.ccnu.edu.cn/roamingAction.do?appId=XK"
login_ticket_url = "http://122.204.187.6/xtgl/login_tickitLogin.html"
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Host": "122.204.187.6",
    "Pragma": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    "Origin": "http://122.204.187.6",
    "Referer": "http://122.204.187.6/cjcx/cjcx_cxDgXscj.html"
}

headers2 = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Cookie": "JSESSIONID=aaaVXuZqChRsa9iHtIvTv; BIGipServerpool_portal=173058240.20480.0000; UM_distinctid=15b5d8be64f12e-0bf2dfe294ca19-396a7805-13c680-15b5d8be65e45",
    "Host": "portal.ccnu.edu.cn",
    "Pragma": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
}

# async def _get_grade(session, payload, ip, sid):
#     grade_url = grade_index_url % sid
#     link_url = link_index_url
#     async with session.get(link_url, timeout=4, headers=headers2, proxy=ip):
#         async with session.get(login_ticket_url, headers=headers, proxy=ip):
#             async with session.post(grade_url, data=payload, headers=headers) as resp:
#                 try:
#                     json_data = await resp.json()
#                     gradeList = []
#                     _gradeList = json_data.get('items')
#                     for _ in _gradeList:
#                         gradeList.append({
#                             'course'  : _.get('kcmc'),
#                             'credit'  : _.get('xf'),
#                             'grade'   : _.get('cj'),
#                             'category': _.get('kclbmc'),
#                             'type'    : _.get('kcgsmc'),
#                             'jxb_id'  : _.get('jxb_id'),
#                             'kcxzmc'  : _.get('kcxzmc')
#                         })
#                     print('got!')
#                     return gradeList
#                 except json.decoder.JSONDecodeError as e:
#                     print(e)
#                     return [None]

async def get_grade(s, sid, ip, xnm, xqm):
    payload = {
        'xnm': xnm, 'xqm': xqm,
        '_search': 'false', 'nd': '1487928673156',
        'queryModel.showCount': 15, 'queryModel.currentPage': 1,
        'queryModel.sortName': "", 'queryModel.sortOrder': 'asc',
        'time': 0
    }
    grade_url = grade_index_url % sid
    async with aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar(unsafe=True),
            cookies=s, headers=headers) as session:
        # rv = await _get_grade(session, payload, ip, sid)
        async with session.post(grade_url, data=payload) as resp:
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
                        'kcxzmc'  : _.get('kcxzmc')
                    })
                print('got!')
                return gradeList
            except json.decoder.JSONDecodeError as e:
                print(e)
                return [None]
            # return rv
