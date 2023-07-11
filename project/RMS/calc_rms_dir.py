# Standard imports
import os
import librosa
import math
import numpy as np
import sys

def get_rms(records):
    """
    均方根值 反映的是有效值而不是平均值
    """
    return math.sqrt(sum([x ** 2 for x in records]) / len(records))

def main():
    DirName = sys.argv[1]
    mono = False
    offset = 2.0 # 1: ppk=1.1255005550562518    2: 1.1198721161739906
    statistics_list = []
    for root, dirs, files in os.walk(DirName):
        for name in files:
            audio_file = os.path.join(root, name)
            if audio_file.endswith('.wav'):
                print(f'计算{audio_file}开始...')
                y, sr = librosa.load(path=audio_file, sr=None, offset=offset, mono=mono)
                if not mono:
                    y = y[0]
                rms_raw = get_rms(y)
                rms_db = math.log(rms_raw, 10) * 20
                statistics_list.append(rms_db)
                print(f'rms_raw={rms_raw}')
                print(f'rms_db ={rms_db}')
                print('计算结束\n')

    # 统计数据的离散程度
    print(f'数据总数={len(statistics_list)}, 数据列表={statistics_list}')
    low_val = -11.7
    super_val = -5.7
    std_val = np.std(statistics_list)
    mean_val = np.mean(statistics_list)
    ppk = min(super_val-mean_val, mean_val-low_val)/3/std_val
    print(f'ppk={ppk}')

if __name__ == '__main__':
    main()
