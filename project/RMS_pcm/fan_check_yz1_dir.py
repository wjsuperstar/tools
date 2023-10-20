import os
import sys
import math
import time
import pandas as pd
import soundfile as sf
import numpy as np
#from scipy.io import wavfile
from scipy.signal import butter, filtfilt

# 对音频进行高通滤波
def highpass_filter(data, cutoff_freq, sample_rate):
    nyquist = 0.5 * sample_rate
    normal_cutoff = cutoff_freq / nyquist
    b, a = butter(5, normal_cutoff, btype='highpass', analog=False)
    filtered_data = filtfilt(b, a, data)
    return filtered_data

# 定义带通滤波器
def bandpass_filter(data, cutoff_low, cutoff_high, sample_rate):
    nyquist = 0.5 * sample_rate
    band = [cutoff_low/nyquist, cutoff_high/nyquist]
    b, a = butter(5, band, btype='bandpass', analog=False)
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
    #filtered_data = bandpass_filter(data, 3100, 4100, sample_rate)
    filtered_data2 = bandpass_filter(data, 7100, 8100, sample_rate)
    rms_raw = get_rms(filtered_data2)
    rms_db = math.log(rms_raw, 10) * 20
    print(rms_db)
    return rms_db

if __name__ == '__main__':
    DirName = sys.argv[1]
    calc_dt = dict()
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
    df.to_excel(f'statistics_bandpass_{time.time():.0f}.xlsx')