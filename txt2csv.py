#!/usr/bin/python
# -*- coding: UTF-8 -*-

import numpy as np
import pandas as pd
 
txt = np.loadtxt(r'D:\test\test_py\playback.txt')
txtDF = pd.DataFrame(txt)
txtDF.to_csv(r'D:\test\test_py\file.csv',index=False)

