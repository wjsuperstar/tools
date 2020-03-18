#!/usr/bin/python
# -*- coding: UTF-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from time import sleep
import json

#json配置文件路径
JsCfgPath="obos_settings.json"
#终端号
DevNumList=[]
# 需要设置哪些参数
VaildParam=[]
# 参数列表
ParamList={}

with open(JsCfgPath, encoding='utf-8') as fd:
    js = json.load(fd)
    ParamList=js["ParamList"]
    VaildParam=js["VaildParam"]
    DevNumList=js["DevNumList"]

# 打开Chrome浏览器
browser = webdriver.Chrome()
browser.get("http://www.o-bos.com:50099/login.jsp")

# 登录
element = browser.find_element_by_id("userName")
element.send_keys("吴建")
element = browser.find_element_by_id("password")
element.send_keys("qaz1144")
browser.find_element_by_xpath("//*[@id='login']/tbody/tr[6]/td[2]/input").click()

#进入任务管理
browser.find_element_by_id("taskdfdiv").click()
#browser.implicitly_wait(1)

#切换窗口
browser.switch_to.window(browser.window_handles[1])
#browser.implicitly_wait(1)

#进入参数设置
browser.switch_to.default_content()
browser.switch_to.frame("left")
browser.find_element_by_link_text("02-设置终端参数").click()
#填充终端号
sleep(1)
browser.switch_to.default_content()
browser.switch_to.frame("tdMainPage")
browser.find_element_by_name("terminalID").send_keys(DevNumList)

for para in VaildParam:
    sleep(1)
    #填充参数ID
    browser.find_element_by_name("paramType").send_keys(ParamList[para["item"]]["pid"])
    #填充参数类型
    s1 = Select(browser.find_element_by_name("paramFormat"))  # 实例化Select
    s1.select_by_value(ParamList[para["item"]]["type"])
    #填充参数值
    browser.find_element_by_name("paramValue").send_keys(para["val"])
    #添加
    browser.find_element_by_xpath('//*[@id="Tbl"]/thead/tr[7]/td/input').click()
    browser.implicitly_wait(10)
    print(ParamList[para["item"]]["desc"])

sleep(2)
#提交
browser.find_element_by_xpath('//*[@id="Tbl"]/thead/tr[8]/td[1]/input').click()
#查询  
browser.switch_to.default_content()
browser.switch_to.frame("left")
browser.find_element_by_link_text("01-查询任务进度").click()
browser.switch_to.default_content()
browser.switch_to.frame("tdMainPage")
browser.find_element_by_name("terminal_id").send_keys(DevNumList)

for i in range(10):
    sleep(1)
    browser.find_element_by_xpath('//*[@id="Tbl"]/thead/tr[4]/td/input').click()
    sleep(1)
    t = browser.find_element_by_xpath('//*[@id="Tbl"]/thead/tr[3]/td[2]/font[1]').text
    print("当前任务状态是%s"%t)
    if t == "3":
        print("Set param Success!")
        break
    sleep(3)

