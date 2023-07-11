#!/usr/bin/python
# -*- coding: UTF-8 -*-
# desc:Analyze imgage PSNR SSIM.
# auth:wujian 2022-11-01
'''
以.dat结尾的文件是NV12格式的yuv图像（原始图像）；
以.jpg结尾的文件是jpg格式的图片。（目标图片）
以.h264结尾的文件是h264格式的一帧数据。（目标图片）
注意：文件命名格式必须要保证文件名字相同，后缀不同。脚本是通过后缀来确认文件类型的。
'''
import sys
import os
import cv2
import numpy as np
from skimage.metrics import peak_signal_noise_ratio
from skimage.metrics import structural_similarity

def calc_psnr(fd_origin, fd_test):
    PSNR = peak_signal_noise_ratio(fd_origin, fd_test)
    SSIM = structural_similarity(fd_origin, fd_test, channel_axis=2)
    return (PSNR, SSIM)

def analyze_image(img_origin_path, img_test_path):
    fd_origin = cv2.imread(img_origin_path)
    fd_test   = cv2.imread(img_test_path)
    return calc_psnr(fd_origin, fd_test)

def yuv2jpg(file):
    with open(file, 'rb') as fd:
        my_shape = (1080*3//2, 1920)
        cv_format = cv2.COLOR_YUV2BGR_NV12
        yuvdata = np.fromfile(fd, dtype=np.uint8)
        print(f'file_size={yuvdata.size}, cv_format={cv_format}')
        yuv = cv2.cvtColor(yuvdata.reshape(my_shape), cv_format)
        #cv2.imshow("COLOR_YUV2RGB_NV21", yuv)
        #cv2.waitKey(0)
        output_file = os.path.splitext(file)[0] + '_yuv.jpg'
        cv2.imwrite(output_file, yuv)
        return (yuv, output_file)

def h2642jpg(file):
    vc = cv2.VideoCapture(file) # 读入视频文件
    if vc.isOpened(): # 判断是否正常打开
        ret, frame = vc.read()
        output_file = os.path.splitext(file)[0] + '_h264.jpg'
        cv2.imwrite(output_file, frame)
        vc.release()
        return (frame, output_file)
    else:
        print('VideoCapture fail')
        return (None, None)

def main():
    print("usage: python xx.py dir")
    print("计算原始yuv图像和目标jpg图片的PSNR(峰值信噪比)和SSIM(结构相似性)")
    DirName = sys.argv[1]
    for root, dirs, files in os.walk(DirName):
        for name in files:
            file_name = os.path.join(root, name)
            if file_name.endswith('.dat'):
                print('计算开始...')
                yuv, output_file = yuv2jpg(file_name)
                dst_file = os.path.splitext(file_name)[0] + '.jpg'
                dst_file2 = os.path.splitext(file_name)[0] + '.h264'
                if os.path.exists(dst_file):
                    print(f'原始yuv图像 = {file_name}, 目标图片 = {dst_file}')
                    PSNR, SSIM  = analyze_image(output_file, dst_file)
                    #fd_test = cv2.imread(dst_file)
                    #PSNR, SSIM = calc_psnr(yuv, fd_test)
                    print(f'PSNR={PSNR}, SSIM={SSIM}')
                elif os.path.exists(dst_file2):
                    print(f'原始yuv图像 = {file_name}, 目标图片 = {dst_file2}')
                    h264, output_file = h2642jpg(dst_file2)
                    PSNR, SSIM = calc_psnr(yuv, h264)
                    print(f'PSNR={PSNR}, SSIM={SSIM}')
                print('计算结束\n')

def test_self():
    yuv, output_file = yuv2jpg(sys.argv[1])
    fd_test = cv2.imread(output_file)
    PSNR, SSIM = calc_psnr(yuv, fd_test)
    print(f'PSNR={PSNR}, SSIM={SSIM}')

def test_jpeg():
    PSNR, SSIM = analyze_image(sys.argv[1], sys.argv[2])
    print(f'PSNR={PSNR}, SSIM={SSIM}')

def test_h264_video():
    frame_cnt = 1
    vc = cv2.VideoCapture(sys.argv[1]) # 读入视频文件
    if vc.isOpened(): # 判断是否正常打开
        while frame_cnt > 0:
            ret, frame = vc.read()  # frame为一帧图像，当frame为空时，ret返回false，否则为true
            if ret:
                cv2.imshow("h.264", frame)
                cv2.waitKey(2000)
            else:
                print('read fail')
            frame_cnt -= 1
        vc.release()
    else:
        print('VideoCapture fail')

def test_h264_pic():
    vc = cv2.VideoCapture(sys.argv[1]) # 读入视频文件
    if vc.isOpened(): # 判断是否正常打开
        ret, frame = vc.read()
        yuv, output_file = yuv2jpg(sys.argv[2])
        PSNR, SSIM = calc_psnr(yuv, frame)
        output_file = os.path.splitext(output_file)[0] + '_h264.jpg'
        cv2.imwrite(output_file, frame)
        print(f'PSNR={PSNR}, SSIM={SSIM}')
        vc.release()
    else:
        print('VideoCapture fail')

if __name__ == '__main__':
    main()
    #test_jpeg()
    #test_self()
