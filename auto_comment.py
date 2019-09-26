#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author: WuJian
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
#from selenium.webdriver.common.action_chains import ActionChains 
from time import sleep

#############以下内容为用户配置项#################
## 你的RDM用户名和密码：
RdmUser="baosisi"
RdmPasswd="123456"
## 评论内容
CommentText="待处理"
## RDM网址
#RdmWeb="http://172.16.1.14:2000/"
RdmWeb="http://rdm.hopechart.com:800/main.do"

#############以下内容为代码，不建议修改###########

# 登录
def LogOn(browser):
    browser.find_element_by_id("userName").send_keys(RdmUser)
    browser.find_element_by_id("userPassword").send_keys(RdmPasswd)
    browser.find_element_by_id("loginBtn").click()
    browser.implicitly_wait(5)

# 获取每页有多少行
def GetRowsInOnePage(browser):
    browser.switch_to.default_content()
    browser.switch_to.frame(0)
    tab=browser.find_element_by_class_name("body-table")
    tr_list = tab.find_elements_by_tag_name('tr')
    return len(tr_list)
# 写一条评论
def AddCommentNote(browser):
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

# 评论一页
def CommnentOnePage(browser):
    row_num = GetRowsInOnePage(browser)
    for row in range(row_num):
        browser.switch_to.default_content()
        browser.switch_to.frame(0)
        sleep(1)
        tr=browser.find_element_by_class_name("body-table").find_elements_by_tag_name('tr')
        td_list=tr[row].find_elements_by_tag_name('td')
        print("----------------------开始评论第%s个任务:" % td_list[0].text)
        print(td_list[2].text)
        #拖动到可见的元素
        browser.execute_script("arguments[0].scrollIntoView();", td_list[2]) 
        tr[row].find_element_by_link_text(td_list[2].text).click()
        sleep(3)
        AddCommentNote(browser);
        sleep(1)
        
def main():
    # 打开Chrome浏览器
    browser = webdriver.Chrome()
    browser.implicitly_wait(5)
    # 打开RDM网址
    browser.get(RdmWeb)
    browser.implicitly_wait(10)
    LogOn(browser)
    while True:
        try:
            CommnentOnePage(browser)
            browser.switch_to.default_content()
            browser.switch_to.frame(0)
            browser.find_element_by_id("pagination_nextPage").click()
            print("进入下一页")
        except ElementNotInteractableException:
            print("哈哈，评论完成，没有下一页啦")
            break
        sleep(2)
    browser.quit()
if __name__ == '__main__':
    main()

