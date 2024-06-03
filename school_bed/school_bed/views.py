from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from spider_model import ModelData
from spider_model import GetMainDiamondData
from datetime import datetime, timedelta


def hello(request):
    return HttpResponse("Hello world ! ")


def submit_data(request):
    today = datetime.now()
    to7day = datetime.now() - timedelta(days=7)
    modelDataTime = ModelData.getAllModelData().GetAllModelTimer(today.strftime("%Y%m%d"), to7day.strftime("%Y%m%d"))
    info1_data = tmpInfoData().info1(7, modelDataTime)
    info1 = {
        "y": [i['diamond'] for i in info1_data],
        "x": [
            f"{i['date'][:4]}年{int(i['date'][4:6])}月{int(i['date'][6:])}日"
            for i in info1_data
        ]
    }


    today = datetime.now()
    to7day = datetime.now() - timedelta(days=14)
    modelDataTime = ModelData.getAllModelData().GetAllModelTimer(today.strftime("%Y%m%d"), to7day.strftime("%Y%m%d"), groupByKey='res_name')
    info2_data = tmpInfoData().info2(modelDataTime)
    info2 = {
        "y": [i['diamond'] for i in info2_data][:7][::-1],
        "x": [i['date'] for i in info2_data][:7][::-1]
    }


    ttd = datetime.now() - timedelta(days=1)
    modelDataTime = ModelData.getAllModelData().GetAllModelTimer(ttd.strftime("%Y%m%d"), ttd.strftime("%Y%m%d"), groupByKey='res_name')
    info3_data = tmpInfoData().info2(modelDataTime)
    info3 = {
        "y": [i['diamond'] for i in info3_data][:7][::-1],
        "x": [i['date'] for i in info3_data][:7][::-1]
    }

    ToMoonDiamond = ModelData.getAllModelData().GetAllModelDiamond(ModelData.getAllModelData().GetAllModel())
    return JsonResponse({
        'status': 'success',
        'ToMoonDiamond': ToMoonDiamond,
        'info1': info1,
        'info2': info2,
        'info3': info3,
    })


def runoob(request):
    view_dict = {
        "data": "测试测试",
        "create": "测试"
    }
    return render(request, "runoob.html", {"views_dict": view_dict})


def view_main(request):
    return render(request, "1.html")


class tmpInfoData:
    def info1(self, days, modelData):
        date_list = []
        current_date = datetime.now()
        for i in range(1, days + 1):
            previous_date = current_date - timedelta(days=i)
            date_string = previous_date.strftime("%Y%m%d")
            date_list.append(date_string)
        data_ = [{
            "diamond": modelData[key]['diamond'],
            "date": key
        } for key in modelData if key in date_list]
        return data_


    def info2(self, modelData):
        data_ = [{
            "diamond": modelData[key]['diamond'],
            "date": key
        } for key in modelData]
        data_ = sorted(data_, key=lambda x: x["diamond"], reverse=True)
        return data_