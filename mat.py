import numpy as np
import matplotlib.pyplot as plt

x = np.arange(0, 5, 0.1)
y = np.sin(x)
plt.plot(x, y, label="deal line")
plt.legend(loc='lower right') #绘制图例
plt.show()



