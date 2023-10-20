import math
import os
import sys
import numpy as np
import openpyxl
import pandas as pd
import librosa
import librosa.display
import matplotlib.pyplot as plt
from openpyxl.drawing.image import Image
import soundfile as sf

g_offset = 1.0
g_mono = False
g_out_excel = 'spectrogram-all.xlsx'

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
        ws.add_image(img, 'C'+str(num))
        num += 1
    wb.save(excel_name)

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
    for root, dirs, files in os.walk(DirName):
        for name in files:
            audio_file = os.path.join(root, name)
            if audio_file.endswith('.pcm'):
                print(f'计算{audio_file}开始...')
                y, sr = sf.read(audio_file, format='RAW', subtype='PCM_16', channels=2, samplerate=48000,
                                dtype=np.float32)
                y = y.T[0]
                # generate picture
                pic_name = os.path.splitext(audio_file)[0] + '.jpg'
                audio_wave2jpg(y, sr, pic_name)
                file_type = audio_file.split(os.path.sep)[2]
                dist_list[audio_file] = [file_type]
                print('计算结束\n')
    df = pd.DataFrame(dist_list, index = ['type', 'spectrogram'])
    df = df.T
    df.to_excel(g_out_excel)
    insert_wave2excel(g_out_excel, dist_list)
if __name__ == '__main__':
    main()