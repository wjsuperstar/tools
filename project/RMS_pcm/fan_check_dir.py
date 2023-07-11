import os
import struct
import sys
import math
import pandas as pd

def main(audio_file):
    #audio_file = sys.argv[1]
    print(f'audio_file={audio_file}')
    with open(audio_file, 'rb') as fd:
        tmp = fd.read()
    line_no = 0
    sum = 0
    numSamples = 0
    while line_no < len(tmp):
        left,right= struct.unpack('<2h', tmp[line_no:line_no+4])
        #print(left,right)
        line_no += 4
        sum += (left*left)
        numSamples += 1
    rms_raw = math.sqrt(sum / numSamples)
    rms_db = math.log(rms_raw/32768, 10) * 20
    print(f'pcm_rms_db ={rms_db}')
    return rms_db

if __name__ == '__main__':
    DirName = sys.argv[1]
    calc_dt = dict()
    out_excel = 'statistics_pcm_file.xlsx'
    for root, dirs, files in os.walk(DirName):
        for name in files:
            audio_file = os.path.join(root, name)
            if audio_file.endswith('.pcm'):
                print(f'计算{audio_file}开始...')
                rms = main(audio_file)
                file_type = audio_file.split(os.path.sep)[1]
                #print(file_type)
                calc_dt[audio_file] = [file_type, rms]
                print('计算结束\n')

    df = pd.DataFrame(calc_dt, index = ['type', 'rms'])
    df = df.T
    df.to_excel(out_excel)