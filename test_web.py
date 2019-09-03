#!/usr/bin/python
# -*- coding: UTF-8 -*-
from selenium import webdriver
#修改项
TaskName=u"自定义状态协议制定"
TaskRate="50"
TaskTime="6"
TaskContext=u"1.制定车辆状态，终端状态，4G信号协议"

# 打开Chrome浏览器
browser = webdriver.Chrome()
browser.get("http://172.16.1.14:2000/")

# 登录
element = browser.find_element_by_id("userName")
element.send_keys("wujian")
element = browser.find_element_by_id("userPassword")
element.send_keys("123456")
browser.find_element_by_id("loginBtn").click()

browser.find_element_by_link_text(u"我的任务").click()
browser.implicitly_wait(1)
#browser.switch_to_frame("main")
browser.switch_to.frame(0)

browser.find_element_by_link_text(TaskName).click()
#browser.find_element_by_link_text(u"专网obos适配").click()
#browser.find_element("title", TaskName).click()

#browser.find_element_by_xpath("//*[@class='body-table']/tbody/tr[1]/td[6]").click();
#ele = browser.find_element_by_id("taskPanel")
#browser.find_element_by_xpath("//table[@class='body-row']/td[6]").click();

#table1 = browser.find_element_by_id("taskInfo")
#table_rows = table1.find_elements_by_tag_name('tr')

#print(table_rows)
#browser.find_element_by_class_name("item-span auto-link").click()
browser.implicitly_wait(1)
browser.switch_to.default_content()
browser.switch_to.frame("main")
browser.switch_to.frame("taskPage")
browser.switch_to.frame("baseInfoFrm")

browser.find_element_by_name("report_rate").send_keys(TaskRate)
browser.find_element_by_name("report_in_work").send_keys(TaskTime)
browser.find_element_by_name("operate_remark").send_keys(TaskContext)

browser.switch_to.parent_frame()
browser.find_element_by_xpath("//*[@id='operateDiv']/input[1]").click()

browser.switch_to.default_content()
browser.find_element_by_xpath("//*[@id='dialogPanel']/div[2]/table/tbody/tr/td[2]/input[1]").click()


