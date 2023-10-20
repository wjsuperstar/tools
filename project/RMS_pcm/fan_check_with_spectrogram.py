import math
import os
import sys
import time
import numpy as np
import openpyxl
import pandas as pd
import librosa
import librosa.display
import matplotlib.pyplot as plt
from openpyxl.drawing.image import Image
import soundfile as sf
from scipy.signal import butter, filtfilt
from scipy.io import wavfile

def get_rms(records):
    """
    均方根值 反映的是有效值而不是平均值
    """
    return math.sqrt(sum([x ** 2 for x in records]) / len(records))

def insert_wave2excel(excel_name, data):
    wb = openpyxl.load_workbook(excel_name, data_only=True)
    ws = wb["Sheet1"]
    num = 2
    for audio_file in data.keys():
        pic_name = os.path.splitext(audio_file)[0] + '.jpg'
        img = Image(pic_name)
        img.height = img.height / 2
        img.width = img.width / 2
        ws.row_dimensions[num].height = 180
        k = openpyxl.utils.get_column_letter(1)
        ws.column_dimensions[k].width = 90
        ws.add_image(img, 'K'+str(num))
        num += 1
    wb.save(excel_name)

# 定义带通滤波器
def bandpass_filter(data, cutoff_low, cutoff_high, sample_rate):
    nyquist = 0.5 * sample_rate
    band = [cutoff_low/nyquist, cutoff_high/nyquist]
    b, a = butter(5, band, btype='bandpass', analog=False)
    filtered_data = filtfilt(b, a, data)
    return filtered_data

def audio_wave2jpg(y, sr, pic_name):
    D = librosa.stft(y)
    D = librosa.amplitude_to_db(np.abs(D), ref=np.max)
    plt.figure()
    librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='log')
    #y_ticks = list(range(2000, 20000, 2000))  # 自定义刻度值
    #plt.yticks(y_ticks, [str(f) + ' Hz' for f in y_ticks])  # 使用刻度值和标签
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectrogram')
    #plt.show()
    plt.savefig(pic_name)
    
def main():
    DirName = sys.argv[1]
    dist_list = dict()
    
    g_out_excel = f'debug_record_all3_{time.time():.0f}.xlsx'
    for root, dirs, files in os.walk(DirName):
        for name in files:
            audio_file = os.path.join(root, name)
            if audio_file.endswith('.pcm'):
                print(f'计算{audio_file}开始...')
                y, sr = sf.read(audio_file, format='RAW', subtype='PCM_16', channels=2, samplerate=48000,
                                dtype=np.float32)
                y = y.T[0]
                # 提取2~8秒的数据
                y = y[2*sr:8*sr]
                # 降噪
                D = librosa.stft(y)
                D = librosa.amplitude_to_db(np.abs(D), ref=np.max)
                spectral_denoised = librosa.decompose.nn_filter(D, aggregate=np.median,metric='cosine', width=int(librosa.time_to_frames(2, sr=sr)))
                y = librosa.istft(spectral_denoised) # 将降噪后的声音转换回时域
                wavfile.write(os.path.splitext(audio_file)[0]+'.wav', 48000, np.array(y, dtype=np.float32))

                # generate picture
                pic_name = os.path.splitext(audio_file)[0] + '.jpg'
                audio_wave2jpg(y, sr, pic_name)
                #过零率
                zcr_all = librosa.feature.zero_crossing_rate(y)[0]
                zcr_all = np.mean(zcr_all)

                filtered_data = []
                filtered_data.append(bandpass_filter(y, 900, 1100, sr))
                filtered_data.append(bandpass_filter(y, 1900, 2100, sr))
                filtered_data.append(bandpass_filter(y, 3900, 4100, sr))
                filtered_data.append(bandpass_filter(y, 7000, 9000, sr))

                rms_db = [math.log(get_rms(i), 10) * 20 for i in filtered_data]
                #zcr    = [np.mean(librosa.feature.zero_crossing_rate(i)[0]) for i in filtered_data]
                
                file_type = audio_file.split(os.path.sep)[2]
                dist_list[audio_file] = [file_type, zcr_all] + rms_db 
                print(dist_list[audio_file])
                print('计算结束\n')
    #df = pd.DataFrame(dist_list, index = ['type', 'ZCR-ALL', 'zcr(900-1100)', 'zcr(1900-2100)', 'zcr(3900-4100)', 'zcr(7000-9000)',
    #                                     'rms(900-1100)', 'rms(1900-2100)', 'rms(3900-4100)', 'rms(7000-9000)'])
    df = pd.DataFrame(dist_list, index = ['type', 'ZCR-ALL', 'rms(900-1100)', 'rms(1900-2100)', 'rms(3900-4100)', 'rms(7000-9000)'])
    df = df.T
    df.to_excel(g_out_excel)
    insert_wave2excel(g_out_excel, dist_list)
if __name__ == '__main__':
    main()