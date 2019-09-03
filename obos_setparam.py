#!/usr/bin/python
# -*- coding: UTF-8 -*-
from selenium import webdriver
#修改项
DevNumList="1903300540"

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
browser.switch_to.frame(0)

#进入参数设置
browser.find_element_by_link_text("02-设置终端参数").click()

#填充终端号
browser.switch_to.default_content()
browser.switch_to.frame("tdMainPage")
browser.find_element_by_name("terminalID").send_keys(DevNumList)




'''
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

'''
