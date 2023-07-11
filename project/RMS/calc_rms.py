# Standard imports
import librosa
import math
#from librosa import load
import os, sys, getopt

import numpy as np

'''
def get_rms(records):
    """
    均方根值 反映的是有效值而不是平均值
    """
    return math.sqrt(sum([x ** 2 for x in records]) / len(records))
'''
def my_std_mfcc(g_offset, g_mono):
    root_path = './'
    if getattr(sys, 'frozen', False):
        root_path = os.path.dirname(sys.executable)
    elif __file__:
        root_path = os.path.dirname(__file__)
    test_file1 = os.path.join(root_path, 'befor.wav')
    #print(f'root_path={root_path}, {test_file1}')
    # 加载音频文件
    y, sr = librosa.load(path=test_file1, sr=None, offset=g_offset, mono=g_mono)
    if not g_mono:
        y = y[0]
    # 提取MFCC特征向量
    mfcc1 = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    # 将MFCC特征向量序列转换为一个特征向量
    return np.mean(mfcc1.T, axis=0)

def display_help():
    print('用法：calc_rms.exe -f 音频文件路径 -j xx -s')
    print('-f 必选参数，音频文件路径')
    print('-j 可选参数，读取音频文件时，从起始时间算，跳几秒，默认1秒')
    print('-s 可选参数，带上该参数说明音频文件要转换成单声道，不带该参数表示不转换, 当前测试音频文件是双声道的，所以不用带')
def parse_cmd_param():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "f:j:s")
    except getopt.GetoptError:
        display_help()
        sys.exit(-1)
    audio_file = None
    mono = False
    jump_sec = 1.0
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            display_help()
            sys.exit(0)
        elif opt in ("-f"):
            audio_file = arg
        elif opt in ("-j"):
            jump_sec = float(arg)
        elif opt in ("-s"):
            mono = True

    if audio_file is None:
        display_help()
        sys.exit(-1)

    return audio_file, jump_sec, mono

def main():
    audio_file, offset, mono = parse_cmd_param()
    print(f'audio_file={audio_file}, offset={offset}, mono={mono}')
    y, sr = librosa.load(path=audio_file, sr = None, offset=offset, mono=mono)
    #print(y, sr)
    if not mono:
        y = y[0]

    std_mfcc = my_std_mfcc(offset, mono)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    curr_mfcc = np.mean(mfcc.T, axis=0)
    mean_mfcc = np.mean(mfcc[0])
    # 计算欧氏距离
    dist = np.linalg.norm(curr_mfcc - std_mfcc)
    # 相似度
    xsd = 1 / (1 + dist) * 100
    # RMS
    rms = librosa.feature.rms(y=y)[0]
    rms_raw = np.mean(rms)
    rms_db = math.log(rms_raw, 10) * 20

    print(f'rms_raw={rms_raw}')
    print(f'rms_db ={rms_db}')
    print(f'dist={dist}, similarity={xsd}')

if __name__ == '__main__':
    main()
