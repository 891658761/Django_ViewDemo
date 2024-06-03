import requests
# 引入数据文件
from school_bed import config as Db
from spider_model.InitCookie import GetUrlData


class GetDefault_Diamond(GetUrlData):
    # 获取主页钻石收益
    def getDiamondData(self):
        url = "https://mc-launcher.webapp.163.com/data_analysis/overview/"
        try:
            data = requests.get(url=url, headers=Db.header, cookies=self.cookie_data).json()['data']
            todayDim = data.get("yesterday_diamond", 0)
            MoonDim = data.get("this_month_diamond", 0)
            todayMon = round((todayDim / 100) * 0.42, 2)
            MoonMon = round((MoonDim / 100) * 0.42, 2)
            return {
                "diamond_today": todayDim,
                "money_today": todayMon,
                "diamond_Moon": MoonDim,
                "money_Moon": MoonMon
            }
        except:
            return {
                "diamond_today": 0,
                "money_today": 0,
                "diamond_Moon": 0,
                "money_Moon": 0
            }
