from datetime import datetime, timedelta

from spider_model import ModelData

from itertools import groupby

class tmpInfoData:
    def info2(self, modelData):
        data_ = [{
            "diamond": modelData[key]['diamond'],
            "date": key
        } for key in modelData]
        data_ = sorted(data_, key=lambda x: x["diamond"], reverse=True)
        return data_

if __name__ == '__main__':
    today = datetime.now()
    to7day = datetime.now() - timedelta(days=14)
    modelDataTime = ModelData.getAllModelData().GetAllModelTimer(today.strftime("%Y%m%d"), to7day.strftime("%Y%m%d"),
                                                                 groupByKey='res_name')
    info2_data = tmpInfoData().info2(modelDataTime)
    info2 = {
        "y": [i['diamond'] for i in info2_data][:7],
        "x": [i['date'] for i in info2_data][:7]
    }
    print(info2)
