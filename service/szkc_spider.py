import asyncio
import aiohttp
import time
import os
from bs4 import BeautifulSoup

pre_url = "http://122.204.187.9/jwglxt"
pre_url2 = "http://122.204.187.9/jwglxt/xtgl/dl_loginForward.html?_t="
login_url = "http://122.204.187.9/jwglxt/xtgl/login_login.html"
table_url = "http://122.204.187.9/jwglxt/kbcx/xskbcx_cxXsKb.html?gnmkdmKey=N253508"
grade_url = "http://122.204.187.9/jwglxt/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdmKey=N305005&sessionUserKey=muxi"
detail_grade_url = "http://122.204.187.9/jwglxt/cjcx/cjcx_cxCjxq.html?gnmkdmKey=N305005&sessionUserKey=muxi"

sid = os.getenv('ADMIN_SID') or "muxi"
pwd = os.getenv('ADMIN_PWD') or "ihdmx123"


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
}


async def login_szkc(sid, pwd):
    async with aiohttp.ClientSession(cookie_jar = aiohttp.CookieJar(unsafe=True),
                                     headers = headers) as session:
        async with session.get(pre_url) as resp:
            if resp.status == 200:
                tlist = str(time.time()).split('.')
                t = tlist[0] + tlist[1][0:3]
                async with session.get(pre_url2 + t) as resp2:
                    if resp2.status == 200:
                        payload = {
                            "yhm": sid,
                            "mm": pwd,
                            "yzm":""
                        }
                        async with session.post(login_url, data = payload) as resp3:
                            resp_text = await resp3.text()
                            loginok = False
                            msg = ""
                            if "用户名或密码不正确" in resp_text:
                                msg = "用户名或密码错误"
                            elif "xskbcx_cxXskbcxIndex.html" in resp_text:
                                loginok = True
                            elif "登录超时" in resp_text:
                                msg = "登录超时"
                            else:
                                msg = "未知错误"

                            cookies = {}
                            if loginok:
                                for cookie in session.cookie_jar:
                                    cookies[cookie.key] = cookie.value
                                print(cookies)
                                return cookies
                            else:
                                print(msg)
                                return {"msg":msg}


async def get_szkc_grade(s, xnm, xqm ):

    """
	获取素质课成绩 
	:param s: 学号
	:param : cookies: jsessionid 和 bigipserverpool
	:param xnm: 学年
	:param xqm: 学期
	:return: 学生素质课成绩
	"""
    cookie = await login_szkc(sid,pwd)
    tlist = str(time.time()).split('.')
    t = tlist[0] + tlist[1][0:3]
    payload = {
        "xnm": xnm,
        "xqm": xqm,
        "xhxm" : s,
        "_search": False,
        "nd": t,
        "queryModel.showCount":100,
        "queryModel.currentPage":1,
        "queryModel.sortName":"",
        "queryModel.sortOrder":"asc",
        "time":0
    }
    async with aiohttp.ClientSession(headers = headers, cookies = cookie) as session:
        async with session.post(grade_url, data = payload) as resp:
            if resp.status == 200 :
                json_data = await resp.json()
                item = json_data['items']
                res = []
                for each in item :
                    jd = ""
                    if "jd" in each :
                        jd = each['jd']

                    one = {
                        "course" : each['kcmc'],
                        "credit" : jd,
                        "grade" : each['cj'],
                        "category" : "素质课",
                        "type" : "素质课",
                        "jxb_id" : each['jxb_id'],
                        "kcxzmc": "素质" + each['kclbmc'][2:]
                    }
                    one = await get_datail_grade(session,s,xnm,xqm,one)
                    print(one)
                    res.append(one)
                return res
    return None

async def get_datail_grade(session,s,xnm,xqm,course) :
    tlist = str(time.time()).split('.')
    t = tlist[0] + tlist[1][0:3]
    detail_url = detail_grade_url + "&time=" + t
   # print(detail_url)
    async with session.post(detail_url,data={
        "xh_id" : s, "jxb_id" : course['jxb_id'], "xnm" : xnm, "xqm" : xqm, "kcmc" : course['course']}) as resp :
        data = await resp.text()
        #print(resp.status)
        #print(data)
        soup = BeautifulSoup(data, 'lxml')
        tbody = soup.tbody
        tr = tbody.find_all('tr')
        #print(tr)
        if (len(tr) == 1): # 总评
            course.update({'usual': '', 'ending': ''})
        elif (len(tr) == 2): # 期末、总评, 素质课没有平时分。。。
            ending = tr[0].find_all('td')[-1].string[:-1]
            course.update({'usual': '','ending': ending})
        elif (len(tr) == 3 ): # 有种课，有期中，期末和总评
            qizhong = tr[0].find_all('td')[-1].string[:-1]
            qimo = tr[1].find_all('td')[-1].string[:-1]
            #print(type(int(float(qimo))))
            #usual = str((float(qizhong)+float(qimo))/2)
            course.update({'usual':qizhong,'ending':qimo})
        return course

async def pre_get_szkc_grade(s,xnm,xqm) :
    res = []
    if xqm == "" :
        items = [3,12,16]
        for each in items :
            res_= await get_szkc_grade(s,xnm,each)
            res.append(res_)
    else :
        res = await get_szkc_grade(s,xnm,xqm)
    return res


if __name__ == '__main__' :
    s = 2016210897
    loop = asyncio.get_event_loop()
    cookies = loop.run_until_complete(login_szkc(sid,pwd))
    if cookies != None :
        print(cookies)
        loop.run_until_complete(pre_get_szkc_grade(s,2016,""))
    loop.close()
