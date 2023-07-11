#!/usr/bin/python
# -*- coding: UTF-8 -*-
# auth:wujian 20191017

import tkinter
from tkinter.messagebox import *

window = tkinter.Tk()
window.withdraw()  # 退出默认 tk 窗口

'''
result = showinfo('提示', '这是一个提示框')
print(f'提示: {result}')

result = showwarning('警告', '这是一个警告框')
print(f'警告: {result}')

result = showerror('错误', '这是一个错误框')
print(f'错误: {result}')
'''


result = askquestion('是(Y) | 否(N)', 'yes or no ?')
print('askquestion: %s'.rjust(18) % result)

result = askyesno('是(Y) | 否(N)', 'True or False ?')
print('askyesno: %s'.rjust(18) % result)

result = askokcancel('确定 | 取消', 'True or False ?')
print('askokcancel: %s'.rjust(18) % result)

result = askretrycancel('重试(R) | 取消', 'True or False ?')
print('askretrycancel: %s'.rjust(18) % result)

result = askyesnocancel('是(Y) | 否(N) | 取消', 'True or False or None')
print('askyesnocancel: %s'.rjust(18) % result)

