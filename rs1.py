#!/usr/bin/env python
# -*- coding:utf-8 -*-
#发布
from RedisHelper import RedisHelper
obj = RedisHelper()
obj.publish('hello')#发布