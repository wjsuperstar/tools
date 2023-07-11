import struct
import sys
import math

def main():
    audio_file = sys.argv[1]
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

if __name__ == '__main__':
    main()
