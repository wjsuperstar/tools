import os
import sys
import math
import pandas as pd
import soundfile as sf
import numpy as np
#from scipy.io import wavfile
from scipy.signal import butter, filtfilt

# 定义高通滤波器
def butter_highpass(cutoff, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return b, a

# 对音频进行高通滤波
def highpass_filter(data, cutoff_freq, sample_rate):
    b, a = butter_highpass(cutoff_freq, sample_rate)
    filtered_data = filtfilt(b, a, data)
    return filtered_data

def get_rms(records):
    """
    均方根值 反映的是有效值而不是平均值
    """
    return math.sqrt(sum([x ** 2 for x in records]) / len(records))

def deal(audio_file):
    data, sample_rate = sf.read(audio_file, format='RAW', subtype='PCM_16', channels=2, samplerate=48000,
                                dtype=np.float32)
    data = data.T[0]
    #print(data, sample_rate, type(data), data.dtype)
    # 高通滤波参数
    cutoff_freq = 9000  # 截止频率，以 Hz 为单位
    #order = 6  # 滤波器阶数

    # 对音频进行高通滤波
    filtered_data = highpass_filter(data, cutoff_freq, sample_rate)
    print(filtered_data, type(filtered_data), filtered_data.dtype)
    rms_raw = get_rms(filtered_data)
    rms_db = math.log(rms_raw, 10) * 20
    return rms_db

if __name__ == '__main__':
    DirName = sys.argv[1]
    calc_dt = dict()
    out_excel = 'statistics_pcm_file_new-9000.xlsx'
    for root, dirs, files in os.walk(DirName):
        for name in files:
            audio_file = os.path.join(root, name)
            if audio_file.endswith('.pcm'):
                print(f'计算{audio_file}开始...')
                rms = deal(audio_file)
                file_type = audio_file.split(os.path.sep)[1]
                #print(file_type)
                calc_dt[audio_file] = [file_type, rms]
                print('计算结束\n')

    df = pd.DataFrame(calc_dt, index = ['type', 'rms'])
    df = df.T
    df.to_excel(out_excel)