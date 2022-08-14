import json
import requests
import os
from xpinyin import Pinyin


class LA:
    def __init__(self, dir):
        self.dir = dir
        self.lives = []

    # 单次爬取json
    def loadJson(self, name):
        try:
            url = f"http://api.hclyz.com:81/mf/json{name}.txt"
            # url = f"http://api.maiyoux.com:81/mf/json{name}.txt"
            req = requests.get(url)
            js = json.loads(req.text)
            return js
        except:
            print(name, "请求失败")
            quit()

    # 循环爬取所有站点
    def circle(self):
        for d in self.dir:
            self.lives.append(f"【{d}】,#genre#")
            if dir[d] == "":
                pinyin = Pinyin().get_pinyin(d, '')
            else:
                pinyin = self.dir[d]
            js = self.loadJson(pinyin)
            self.lives.extend(f"{j['title']},{j['address']}" for j in js['zhubo'])
            self.lives.append("")
            print(d, "爬取完成")

    # 保存lives
    def save(self, savepath):
        with open(savepath, 'w') as f:
            for live in self.lives:
                f.write(live+"\n")
        pass


# github上传
def git(path):
    """
        git add .
        git commit -m "注释内容"
        git push origin main
    :param path:
    :return:
    """
    order_arr = [f"git add {path}", "git commit -m " + '"' + "直播接口" + '"', "git push origin master"]
    for order in order_arr:
        os.system(order)


if __name__ == '__main__':
    # 设置站点
    dir = {
        "卡哇伊": 'kawayi',
        "蜜桃": 'mitao',
        "夜妖姬": 'yeyaoji',
        "咪咪": 'mimi',
        "蚊香社": 'wenxiangshe',
        "小辣椒": 'xiaolajiao',
        "龙珠": 'longzhu',
        "番茄社区": 'fanjiashequ',
        "LOVE": 'love',
        "小妲己": 'xiaodaji',
        "77直播": '77zhibo',
        "依依": 'yiyi',
        "日出": 'richu',
        "彩虹": 'caihong',
        "久久": 'jiujiu',
        "亚米": 'yami',
        "蝶恋": 'dielian',
        "映客": 'yingke',
        "套路": 'taolu',
        "樱花": 'yinghua',
        "享色": 'xiangse',
        "红浪漫": 'honglangman',
        "金鱼": 'jinyu',
        "桃花": 'taohua',
        "花房": 'huafang',
        "小仙女": 'xiaoxiannu',
        "视觉秀": 'shijuexiu',
        "小天使": 'xiaotianshi',
        "一直播": 'yizhibo',
        "彩云": '',
        "暗语": '',
        "娇媚": '',
        "黄瓜": '',
        "色趣": '',
        "糯米": '',
        "小蜜蜂": '',
        "小红帽": '',
        "桃花运": '',
        "苦瓜": '',
        "爱爱你": '',
        "樱花雨i": '',
        "盘他": '',
        "夜色": '',
        "蝴蝶": '',
        "小天仙": '',
        "杏趣": '',
        "小坏蛋": '',
        "飘雪": '',
        "樱桃": '',
        "奥斯卡": 'aosika',
        "卡路里": 'kaluli',
        "红高粱": '',
        "付宝": '',
        "小黄书": '',
        "二嫂": '',
        "花果山": '',
        "云鹿": '',
        "菠萝": '',
        "星宝贝": '',
        "夜艳": '',
        "七仙女s": 'qixiannus',
        "夜来香": '',
        "爱零": '',
        "十八禁": '',
        "兰桂坊": '',
        "Dancelife": '',
        "小萌猪": '',
        "蝴蝶飞": '',
        "幽梦": '',
        "丽柜厅": '',
        "蛟龙": '',
        "颜如玉": '',
        "橙秀": '',
        "鲍鱼l": '',
        "小花螺": '',
        "皇后": '',
        "心之恋": '',
        "台妹l": '',
        "爱恋": '',
        "903娱乐": '',
        "尤物岛": '',
        "坦克": '',
        "好基友": '',
        "夜女郎": 'yenulang',
        "娇喘": '',
        "芒果派": '',
        "媚颜": '',
        "风流": '',
        "夜律": 'yelu',
        "玲珑": '',
        "浴火": '',
        "翠鸟": '',
        "幸运星": '',
        "她秀": '',
        "招财猫": '',
        "双碟": '',
        "糖果": '',
        "么么哒": '',
        "小性感": '',
        "小喵宠": '',
        "兔女郎": 'tunulang',
        "睡美人": '',
        "金呗": '',
        "美夕": '',
        "小妖": '',
        "约直播": '',
        "花仙子": '',
        "土豪": '',
        "红装": '',
        "妞妞": '',
        "艳后": '',
        "moon": '',
        "蓝猫": '',
        "美人妆": '',
        "入巷": '',
        "持久男": '',
        "倾心": '',
        "小精灵": '',
        "偶遇": '',
        "灰灰": '',
        "猫头鹰": '',
        "喜欢你": '',
        "夜纯": '',
        "杏播": '',
        "名流": '',
        "花蝴蝶": '',
        "咪狐": '',
        "牵手": '',
        "情趣": '',
        "蓝月亮": '',
        "小棉袄": ''
    }
    # lives存储地址
    path = "lives/LiveAdult.txt"
    savepath = os.path.join(os.getcwd(), path)
    # 爬取lives
    LA = LA(dir)
    js = LA.circle()
    # 保存lives
    LA.save(savepath)
    # 上传git
    git(path)

