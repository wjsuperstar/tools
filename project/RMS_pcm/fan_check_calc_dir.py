import os
import sys
import math
import time
import pandas as pd
import soundfile as sf
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, filtfilt

g_min_freq = 100
g_max_freq = 20100
g_freq_offset = 1000

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
    rms_list = []
    for freq in range(g_min_freq, g_max_freq, g_freq_offset):
        filtered_data = bandpass_filter(data, freq, freq+g_freq_offset, sample_rate)
        rms_raw = get_rms(filtered_data)
        rms_db = math.log(rms_raw, 10) * 20
        #print('wj:', rms_raw, rms_db)
        rms_list.append(rms_db)
        wav_path = os.path.splitext(audio_file)[0]
        if not os.path.exists(wav_path):
            os.mkdir(wav_path)
        wavfile.write(wav_path+os.path.sep+f'{freq}-{freq+g_freq_offset}HZ'+'.wav', 48000, np.array(filtered_data, dtype=np.float32)) #np.array(filtered_data, dtype=np.int16)
    #print(rms_list)
    return rms_list

if __name__ == '__main__':
    DirName = sys.argv[1]
    calc_dt = dict()
    excel_col_name = []
    for freq in range(g_min_freq, g_max_freq, g_freq_offset):
        excel_col_name.append(f'RMS({freq}~{freq+g_freq_offset}HZ)')
    print(excel_col_name)
    for root, dirs, files in os.walk(DirName):
        for name in files:
            audio_file = os.path.join(root, name)
            if audio_file.endswith('.pcm'):
                print(f'计算{audio_file}开始...')
                rms = deal(audio_file)
                #file_type = audio_file.split(os.path.sep)[1]
                #print(file_type)
                calc_dt[audio_file] = rms
                print('计算结束\n')
                #exit()

    df = pd.DataFrame(calc_dt, index = excel_col_name)
    df = df.T
    df.to_excel(f'statistics_pcm_file_{time.time():.0f}.xlsx')