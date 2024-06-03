from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import json
import os
import requests
# 引入数据文件
from school_bed import config as Db


class GetUrlData:
    def __init__(self):
        self.cookie_data = self.cookie_init()

    def cookie_init(self):
        file_path = "cookie.json"
        if not os.path.exists(file_path):
            cookie_data = self.getCookies()
            with open(file_path, "w") as json_file:
                json.dump(cookie_data, json_file)
            return cookie_data
        else:
            with open(file_path, 'r') as file:
                ck = json.load(file)
            url = "https://mc-launcher.webapp.163.com/data_analysis/overview/"
            try:
                var = requests.get(url=url, headers=Db.header, cookies=ck).json()['data']
                return ck
            except:
                cookie_data = self.getCookies()
                with open(file_path, "w") as json_file:
                    json.dump(cookie_data, json_file)
                return cookie_data

    def getCookies(self):
        opt = Options()
        opt.add_argument("--headless")
        opt.add_argument("--disable-gpu")
        opt.add_argument("--no-sandbox")
        opt.add_argument("--disable-dev-shm-usage")
        opt.add_experimental_option('excludeSwitches', ['enable-logging'])
        web = Chrome(options=opt)
        web.get("https://mcdev.webapp.163.com/#/login")
        time.sleep(3)
        iframe = web.find_element(By.XPATH, '/html/body/div/div/div[1]/div[2]/iframe')
        web.switch_to.frame(iframe)
        time.sleep(3)
        web.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[2]/form/div/div[1]/div[2]/input').send_keys(
            Db.userName)
        web.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[2]/form/div/div[3]/div[2]/input[2]').send_keys(
            Db.passWord)
        time.sleep(2)
        web.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[2]/form/div/div[8]/a').click()
        time.sleep(5)

        cookie_dit = {}
        for dic in web.get_cookies():
            key = dic['name']
            value = dic['value']
            cookie_dit[key] = value

        return cookie_dit
