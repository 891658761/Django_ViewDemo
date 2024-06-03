from spider_model.InitCookie import GetUrlData
import requests
from datetime import datetime, timedelta
from itertools import groupby

from school_bed import config as Db

class getAllModelData(GetUrlData):
    # 判断当前是几号，如果是20号之前，就获取上个月的，如果是20号之后，就获取这个月的
    def getNowTime(self):
        current_date = datetime.now()
        if current_date.day >= 20:
            current_month = current_date.month
            current_year = current_date.year
            date_1 = datetime(current_year, current_month, 20)
            date_2 = datetime(current_year, current_month - 1, 20) if current_month > 1 else datetime(current_year - 1,
                                                                                                      12, 20)
        else:
            current_month = current_date.month
            current_year = current_date.year
            date_1 = datetime(current_year, current_month - 1, 20) if current_month > 1 else datetime(current_year - 1,
                                                                                                      12, 20)
            date_2 = datetime(current_year, current_month - 2, 20) if current_month > 2 else datetime(current_year - 1,
                                                                                                      12 if current_month == 1 else 11,
                                                                                                      20)
        return date_1, date_2

    # 获取组件id列表
    def getAllModelCount(self):
        url = "https://mc-launcher.webapp.163.com/items/categories/pe"
        data = requests.get(url=url, headers=Db.header, cookies=self.cookie_data)
        if data.status_code == 200:
            urlCount = data.json()['data']['count']
            # 每次爬10条
            step = 10
            allModId = []
            for i in range(0, urlCount // step + 1):
                st = 0 + (i * step)
                ed = (i * step) + step
                url2 = "https://mc-launcher.webapp.163.com/items/categories/pe/?start={}&span={}".format(st, step)
                data2 = requests.get(url=url2, headers=Db.header, cookies=self.cookie_data)
                if data2.status_code == 200:
                    for e in data2.json()['data']['item']:
                        allModId.append({
                            "mod_id": e['item_id'],
                            "mod_name": e['item_name'],
                            "star_time": e['create_time'].replace("000+00:00", "Z")
                        })
                else:
                    continue
            return allModId
        else:
            return []

    # 获取指定时间段内的组件收益
    def getTimerModelDiamond(self, Time1, Time2, allModId, groupByKey):
        new_modIdList = [i['mod_id'] for i in allModId]
        # 格式化时间为指定格式
        new_time = Time1 if type(Time1) == str else Time1.strftime("%Y%m%d")
        old_time = Time2 if type(Time2) == str else Time2.strftime("%Y%m%d")
        url2 = "https://mc-launcher.webapp.163.com/data_analysis/day_detail/"
        data_ = {
            "platform": "pe",
            "category": "pe",
            "start_date": old_time,
            "end_date": new_time,
            "item_list_str": ",".join(new_modIdList),
            "sort": "dateid",
            "order": "ASC",
            "start": 0,
            "span": 999999
        }
        data2 = requests.get(url=url2, headers=Db.header, cookies=self.cookie_data, params=data_)
        json_data_ = data2.json()['data']
        # 使用groupby函数按照指定的key进行聚类
        grouped_data = {}
        if json_data_:
            modeDiamondData = json_data_['data']
            for key, group in groupby(modeDiamondData, key=lambda x: x[groupByKey]):
                if key in grouped_data:
                    grouped_data[key] += list(group)
                else:
                    grouped_data[key] = list(group)
        return grouped_data

    # # 获取指定时间段内的组件收益
    # def getTimerModelDiamond_(self, Time1, Time2, allModId):
    #     allModelData = {}
    #     # 格式化时间为指定格式
    #     formatted_current_time = Time1.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    #     formatted_one_year_ago = Time2.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    #     for modi in allModId:
    #         url2 = "https://mc-launcher.webapp.163.com/items/categories/pe/{}/incomes/?begin_time={}&end_time={}".format(
    #             modi['mod_id'], formatted_one_year_ago, formatted_current_time)
    #         data2 = requests.get(url=url2, headers=Db.header, cookies=self.cookie_data)
    #         # 处理未上架的组件
    #         if data2.json().get("msg", None) == "暂无法查询收益，请稍后重试":
    #             continue
    #         mod_allDiamond = data2.json()['data']['total_diamonds']
    #         mod_count = data2.json()['data']['count']
    #         # 处理免费组件
    #         if mod_allDiamond <= 0:
    #             continue
    #         getMoney = round(mod_allDiamond * 0.0042, 2)
    #         allModelData[modi['mod_name']] = {
    #             "ModId": modi['mod_id'],
    #             "ModName": modi['mod_name'],
    #             "ModDownload": mod_count,
    #             "Diamond": mod_allDiamond,
    #             "Money": getMoney
    #         }
    #         print("正在获取模组[{}] {}~{}日期内的数据".format(modi['mod_name'], Time1.strftime("%Y年%m月%d日"), Time2.strftime("%Y年%m月%d日")))
    #         # print("模组{}, 下载量{}, 收益为{}".format(modi['mod_name'], mod_count, getMoney))
    #     return allModelData

    def GetAllModelTimer(self, time1, time2, groupByKey='dateid'):
        allModId = self.getAllModelCount()
        # 如果id列表存在，则继续
        if allModId:
            allModelData = self.getTimerModelDiamond(time1, time2, allModId, groupByKey)
            print(allModelData)
            dic = {}
            for key in allModelData:
                data_ = allModelData[key]
                diamond_ = sum([i.get("diamond", 0) for i in data_])
                download_ = sum([i.get("download_num", 0) for i in data_])
                dic[key] = {
                    "diamond": diamond_,
                    "download": download_,
                    "data": data_
                }
            return dic
        else:
            return {}

    def GetAllModel(self, groupByKey='dateid'):
        allModId = self.getAllModelCount()
        # 如果id列表存在，则继续
        if allModId:
            time1, time2 = self.getNowTime()
            allModelData = self.getTimerModelDiamond(time1, time2, allModId, groupByKey)
            dic = {}
            for key in allModelData:
                data_ = allModelData[key]
                diamond_ = sum([i.get("diamond", 0) for i in data_])
                download_ = sum([i.get("download_num", 0) for i in data_])
                dic[key] = {
                    "diamond": diamond_,
                    "download": download_,
                    "data": data_
                }
            return dic
        else:
            return {}

    def GetAllModelDiamond(self, modelData):
        alldiamond = sum([modelData[i]['diamond'] for i in modelData])
        todayData = {
            "Diamond": alldiamond,
            "Money": round((alldiamond / 100) * 0.42, 2)
        }
        return todayData

