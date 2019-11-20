#!/usr/bin/python
# -*- coding: UTF-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from time import sleep

# 修改项
DevNumList="1909260467"
#DevNumList="1906130556"
# 需要设置哪些参数
#VaildParam=["NpvMainIpC1", "NpvMainPortC1", "Vin", "ObosForever", "NpvGbTestMode"]
#VaildParam=["Vin", "ObosForever", "NpvGbTestMode"]
#VaildParam=["SshEn", "ObosForever"]
#VaildParam=["PartsCode"]

VaildParam=["SshEn", "SshPort", "SshIp", "ObosForever"]

# 参数列表
ParamList={"NpvMainIpC1":    ["0x1000000", "String", "121.196.244.159"],
           "NpvMainPortC1":  ["0x1000001", "Word",   "8111"],
           "NpvbakIpC1":     ["0x1000002", "String", "121.196.244.159"],
           "NpvbakPortC1":   ["0x1000003", "Word",   "8111"],
           "NpvMainIpC2":    ["0x1010000", "String", "121.196.244.159"],
           "NpvMainPortC2":  ["0x1010001", "Word",   "8111"],
           "NpvbakIpC2":     ["0x1010002", "String", "121.196.244.159"],
           "NpvbakPortC2":   ["0x1010003", "Word",   "8111"],
           "Vin":            ["0x3000001", "String", "00000001812120001"],
           "ObosForever":    ["0x30000B1", "DWord",  "99999"],
           "NpvGbTestMode":  ["0x30000AA", "DWord",  "1"],
           "WakeUpMask":     ["0x300102F", "DWord",  "133121"],
           "CanRecEn":       ["0x3000092", "Byte",   "0"],
           "GpsLogEn":       ["0x3000096", "DWord",  "1"],
           "NpvLogEn":       ["0x300009C", "DWord",  "1"],
           "SshEn":          ["0x30000D9", "DWord",  "1"],
           "SshPort":        ["0x30000DB", "Word",   "7467"],
           "SshIp":          ["0x30000DA", "String", "47.111.129.182"],
           "NpvHistFilePa":  ["0x300001C", "String",  "/media/card/data/queuefile/data_npv_chn"],
           "PartsCode":      ["0x300F506", "String",  "ZQ01169880"],
        
        }
    

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

for i in range(len(VaildParam)):
    sleep(1)
    #填充参数ID
    browser.find_element_by_name("paramType").send_keys(ParamList[VaildParam[i]][0])
    #填充参数类型
    s1 = Select(browser.find_element_by_name("paramFormat"))  # 实例化Select
    s1.select_by_value(ParamList[VaildParam[i]][1])
    #填充参数值
    browser.find_element_by_name("paramValue").send_keys(ParamList[VaildParam[i]][2])
    #添加
    browser.find_element_by_xpath('//*[@id="Tbl"]/thead/tr[7]/td/input').click()
    browser.implicitly_wait(10)

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

