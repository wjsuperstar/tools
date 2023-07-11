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

g_offset = 1.0
g_mono = False
g_out_excel = 'test.xlsx'

def insert_wave2excel(excel_name, data):
    wb = openpyxl.load_workbook("test.xlsx", data_only=True)
    ws = wb["Sheet1"]
    num = 2
    for audio_file in data.keys():
        pic_name = os.path.splitext(audio_file)[0] + '.jpg'
        img = Image(pic_name)
        img.height = img.height / 4
        img.width = img.width / 2
        ws.row_dimensions[num].height = 100
        ws.add_image(img, 'G'+str(num))
        num += 1
    wb.save("test_with_pic.xlsx")

def audio_wave2jpg(y, sr, pic_name):
    plt.figure()
    librosa.display.waveshow(y, sr=sr, max_points=24000 * 10000)
    plt.xlim(2.1, 2.105)
    plt.savefig(pic_name)

def my_std_mfcc():
    test_file1 = r'befor.wav'
    # 加载音频文件
    y, sr = librosa.load(path=test_file1, sr=None, offset=g_offset, mono=g_mono)
    if not g_mono:
        y = y[0]
    # 提取MFCC特征向量
    mfcc1 = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    # 将MFCC特征向量序列转换为一个特征向量
    return np.mean(mfcc1.T, axis=0)

def main():
    DirName = sys.argv[1]
    dist_list = dict()
    std_mfcc = my_std_mfcc()
    for root, dirs, files in os.walk(DirName):
        for name in files:
            audio_file = os.path.join(root, name)
            if audio_file.endswith('.wav'):
                print(f'计算{audio_file}开始...')
                y, sr = librosa.load(path=audio_file, sr=None, offset=g_offset, mono=g_mono)
                if not g_mono:
                    y = y[0]
                mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
                curr_mfcc = np.mean(mfcc.T, axis=0)
                mean_mfcc = np.mean(mfcc[0])
                # 计算欧氏距离
                dist = np.linalg.norm(curr_mfcc - std_mfcc)
                # 相似度
                xsd = 1 / (1 + dist) * 100
                # RMS
                rms = librosa.feature.rms(y=y)[0]
                rms_mean = np.mean(rms)
                rms_db = math.log(rms_mean, 10) * 20
                dist_list[audio_file] = [mean_mfcc, dist, xsd, rms_mean, rms_db]
                # generate wave picture
                pic_name = os.path.splitext(audio_file)[0] + '.jpg'
                audio_wave2jpg(y, sr, pic_name)
                print('计算结束\n')
    df = pd.DataFrame(dist_list, index = ['mfcc[0]', 'dist', 'simulate', 'rms_raw', 'rms_db'])
    df = df.T
    df.to_excel(g_out_excel)
    insert_wave2excel(g_out_excel, dist_list)
if __name__ == '__main__':
    main()