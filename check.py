import json
import requests
import os
import re
from concurrent.futures import ThreadPoolExecutor


# 创建一个xstr类，用于处理从文件中读出的字符串
class xstr:
    def __init__(self, instr):
        self.instr = instr

    # 删除“//”标志后的注释
    def rmCmt(self):
        qtCnt = cmtPos = slashPos = 0
        rearLine = self.instr
        # rearline: 前一个“//”之后的字符串，
        # 双引号里的“//”不是注释标志，所以遇到这种情况，仍需继续查找后续的“//”
        while rearLine.find('//') >= 0: # 查找“//”
            slashPos = rearLine.find('//')
            cmtPos += slashPos
            headLine = rearLine[:slashPos]
            while headLine.find('"') >= 0: # 查找“//”前的双引号
                # print(headLine)
                qtPos = headLine.find('"')
                # print(qtPos)
                if not self.isEscapeOpr(headLine[:qtPos]): # 如果双引号没有被转义
                    qtCnt += 1 # 双引号的数量加1
                    # print("双引号的数量", qtCnt)
                headLine = headLine[qtPos+1:]
            if qtCnt % 2 == 0: # 如果双引号的数量为偶数，则说明“//”是注释标志
                return self.instr[:cmtPos]
            rearLine = rearLine[slashPos+2:]
            cmtPos += 2
        return self.instr

    # 判断是否为转义字符
    def isEscapeOpr(self, instr):
        if len(instr) <= 0:
            return False
        cnt = 0
        while instr[-1] == '\\':
            cnt += 1
            instr = instr[:-1]
            if len(instr) == 0:
                break
        if cnt % 2 == 1:
            return True
        else:
            return False


# 从json文件的路径JsonPath读取该文件，返回json对象
def loadJson(JsonPath):
    try:
        srcJson = open(JsonPath, 'r', encoding="utf-8")
    except:
        print(JsonPath, "打开失败")
        quit()

    dstJsonStr = ''
    for line in srcJson.readlines():
        if not re.match(r'\s*//', line) and not re.match(r'\s*\n', line):
            xline = xstr(line)
            dstJsonStr += xline.rmCmt()

    try:
        dstJson = json.loads(dstJsonStr)
        return dstJson
    except:
        print(JsonPath + '不是json文件')
        quit()


def check(url):
    print("######################")
    print(url)
    try:
        res = requests.get(url, timeout=(20, 60))
        code = res.status_code
    except:
        code = 0
    return code


def th(i, s):
    try:
        ext = s['ext']
        api = s['api']
        if api[:6] == "csp_XP":
            json_s = os.path.join(os.path.abspath(os.path.dirname(path)), ext[7:])
            j = loadJson(json_s)
            url = j['homeUrl']
            code = check(url)
            # with open(json_s, 'r', encoding="utf-8") as j:
            #     url = json.load(j)['homeUrl']
            #     code = check(url)
        if api[:6] == "csp_XB":
            json_s = os.path.join(os.path.abspath(os.path.dirname(path)), ext[7:])
            j = loadJson(json_s)
            # print(j)
            url = j['url']
            code = check(url)
        elif api[:6] == "csp_Ap":
            url = ext
            code = check(url)
    except:
        url = s['api']
        if url[:4] == "http":
            code = check(url)
        else:
            return
    if code != 200:
        print(i, s['name'], code)
        return {'id': i}
    else:
        print(i, s['name'], code)
        return

def parse(res):
    res = res.result()  # !取到res结果 【回调函数】带参数需要这样
    global useless
    try:
        useless.append(res['id'])
        print(f"{res['id']}号源失效")
    except:
        pass


if __name__ == '__main__':
    path = os.getcwd()
    json_name = 'xm1.json'
    # json_main = json.load(open(json_name, 'r', encoding="utf-8"))
    json_main = loadJson(json_name)
    sites = json_main['sites']
    global useless
    useless = []
    pool = ThreadPoolExecutor(5)
    for i, s in enumerate(sites):
        # num = th(i, s)
        pool.submit(th, i,s).add_done_callback(parse)
        # results.append(result)
    pool.shutdown()
    # pool.close()
    # pool.join()
    #
    # useless = [i.get() for i in results]
    # sorted(useless)
    useless = sorted(useless, reverse=True)
    print(useless)
    for u in useless:
        sites.pop(u)

    json_main['sites'] = sites
    print(json_main)
    with open("out_xm.json", 'w', encoding="utf-8") as out:
        json.dump(json_main, out, indent=4, ensure_ascii=False)

