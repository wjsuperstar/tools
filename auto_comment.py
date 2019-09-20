#!/usr/bin/python
# -*- coding: UTF-8 -*-
from selenium import webdriver

#############以下内容为用户配置项#################
## 你的RDM用户名和密码：
RdmUser="wujian"
RdmPasswd="123456"
## 评论内容
CommentText="任务太多，稍后处理"
## RDM网址
RdmWeb="http://172.16.1.14:2000/"


#############以下内容为代码，不建议修改###########
# 打开Chrome浏览器
browser = webdriver.Chrome()
browser.implicitly_wait(5)
# 打开RDM内网网址
browser.get(RdmWeb)

# 登录
browser.find_element_by_id("userName").send_keys(RdmUser)
browser.find_element_by_id("userPassword").send_keys(RdmPasswd)
browser.find_element_by_id("loginBtn").click()

#browser.find_element_by_link_text(u"我的流程").click()
#browser.implicitly_wait(2)
#browser.refresh()
browser.switch_to.frame("main")

task_tab=browser.find_element_by_id('bodyPanel')
print("---------1---------------")
print(task_tab)

tr_list=task_tab.find_elements_by_tag_name('tr')
print("---------3---------------")
print(tr_list)
print("---------4---------------")

print(len(tr_list))

for row in tr_list:
    print(row.text + '\t',end='')


'''
//*[@id="bodyPanel"]/table[1]/tbody

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

driver = webdriver.Firefox()
 3 driver.get(r'file:///D:/pythonSeleniumTestCode/pythonStu/src/table.html')
 4 #id定位方式获取整个表格对象
 5 table = driver.find_element_by_id('table')
 6 #通过标签名获取表格中所有行
 7 trlist = driver.find_elements_by_tag_name('tr')
 8 print(len(trlist))
 9 for row in trlist:
10     #遍历行对象，获取每一个行中所有的列对象
11     tdlist = row.find_elements_by_tag_name('td')
12     for col in tdlist:
13         print(col.text + '\t',end='')
14     print('\n')
15 driver.quit()




browser.quit()
'''