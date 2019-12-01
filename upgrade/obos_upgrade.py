#!/usr/bin/python
# -*- coding: UTF-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from time import sleep
import os

# 终端号
#DevNumList="1911110623"
DevNumList="1911110623"

# 上传目录
UpDir="wj"
# 待上传的升级文件名（包含路径）
FilePathName=r"D:\test\test_py\upgrade\sany.zip"

DevOpt=1


# 打开Chrome浏览器
browser = webdriver.Chrome()
browser.get("http://www.o-bos.com:50099/login.jsp")

# 登录
element = browser.find_element_by_id("userName")
element.send_keys("吴建")
element = browser.find_element_by_id("password")
element.send_keys("qaz1144")
browser.find_element_by_xpath("//*[@id='login']/tbody/tr[6]/td[2]/input").click()

# 进入任务管理
browser.find_element_by_id("taskdfdiv").click()
#browser.implicitly_wait(1)

# 切换窗口
browser.switch_to.window(browser.window_handles[1])
#browser.implicitly_wait(1)

# 切换到更新文件菜单
browser.switch_to.default_content()
browser.switch_to.frame("left")
browser.find_element_by_link_text("01-上传更新文件到网关").click()
browser.implicitly_wait(10)
# 上传升级文件
browser.switch_to.default_content()
browser.switch_to.frame("tdMainPage")
browser.find_element_by_name("saveFile").send_keys("\\"+UpDir)
browser.find_element_by_name("gateFileName").send_keys(FilePathName)
sleep(2)
browser.find_element_by_name("btn1").click()
# 点击弹出里面的确定按钮
browser.switch_to_alert().accept()
sleep(2)

#切换到下发菜单
browser.switch_to.default_content()
browser.switch_to.frame("left")
browser.find_element_by_link_text("02-ABOS终端软件更新").click()
browser.implicitly_wait(10)
browser.switch_to.default_content()
browser.switch_to.frame("tdMainPage")
browser.find_element_by_name("terminalID").send_keys(DevNumList)
browser.find_element_by_xpath('//*[@id="Tbl"]/thead/tr[4]/td[2]/input').send_keys(DevOpt)
browser.find_element_by_name("content").send_keys(UpDir+"\\"+os.path.basename(FilePathName))
sleep(1)
browser.find_element_by_name("btn1").click()
browser.implicitly_wait(10)

#查询  
browser.switch_to.default_content()
browser.switch_to.frame("left")
browser.find_element_by_link_text("01-查询任务进度").click()
browser.switch_to.default_content()
browser.switch_to.frame("tdMainPage")
browser.find_element_by_name("terminal_id").send_keys(DevNumList)

for i in range(30):
    browser.find_element_by_xpath('//*[@id="Tbl"]/thead/tr[4]/td/input').click()
    sleep(5)
    t = browser.find_element_by_xpath('//*[@id="Tbl"]/thead/tr[3]/td[2]/font[1]').text
    print("当前任务状态是%s"%t)
    if t == "3":
        print("upgrade Success!")
        break
    sleep(5)

#browser.quit()
