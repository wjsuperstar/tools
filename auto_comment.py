#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author: WuJian
from selenium import webdriver
from time import sleep

#############以下内容为用户配置项#################
## 你的RDM用户名和密码：
RdmUser="wujian"
RdmPasswd="123456"
## 评论内容
CommentText="任务太多，稍后处理"
## RDM网址
#RdmWeb="http://172.16.1.14:2000/"
RdmWeb="http://rdm.hopechart.com:800/main.do"

#############以下内容为代码，不建议修改###########
# 打开Chrome浏览器
browser = webdriver.Chrome()
browser.implicitly_wait(5)
# 打开RDM网址
browser.get(RdmWeb)

# 登录
browser.find_element_by_id("userName").send_keys(RdmUser)
browser.find_element_by_id("userPassword").send_keys(RdmPasswd)
browser.find_element_by_id("loginBtn").click()

#browser.find_element_by_link_text(u"我的流程").click()
browser.implicitly_wait(5)
browser.switch_to.frame(0)
tab=browser.find_element_by_class_name("body-table")
tr_list = tab.find_elements_by_tag_name('tr')
#进行评论
def AddCommentNote():
    browser.switch_to.default_content()
    browser.switch_to.frame("main")
    browser.switch_to.frame("workflowFrame")
    browser.switch_to.frame("tabs_panel_0")
    browser.find_element_by_id("addNoteBtn").click() 
    browser.implicitly_wait(5)
    browser.find_element_by_id("noteArea").send_keys(CommentText)
    browser.implicitly_wait(5)
    browser.find_element_by_id("saveNoteBtn").click()
    browser.implicitly_wait(5)
    browser.switch_to.default_content()
    browser.find_element_by_xpath('/html/body/div[3]/img').click()
    
for row in range(len(tr_list)):
    print("----------------------开始评论第%d个任务:" % row)
    browser.switch_to.default_content()
    browser.switch_to.frame(0)
    tr=browser.find_element_by_class_name("body-table").find_elements_by_tag_name('tr')
    td_list=tr[row].find_elements_by_tag_name('td')
    print(td_list[2].text)
    tr[row].find_element_by_link_text(td_list[2].text).click()
    sleep(3)
    AddCommentNote();
    sleep(1)

#browser.quit()