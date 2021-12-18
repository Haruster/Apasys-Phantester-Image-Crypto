# Haruster AES_Image_Decrypt.py

import tensorflow
import cv2
import random
import string
from Crypto.Cipher import AES
from PIL import Image
from tensorflow import keras

filename = 'image_encrypted_ecb.bmp'

filename_decrypted_ecb = "image_decrypted_ecb"
format = "png" # format을 png 확장자로 한다.

# key_genarator 함수는 소문자 16개의 문자열을 임의로 생성한다.

'''
def key_generator(size = 16, chars = string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))
'''

# AES 암호화의 텍스트 공간은 16개의 정수 배수로 균등하게 나눌 수 없으므로 이를 채워야하며,
# 해당 아스키코드(ASCII)에서 "\x00"은 0x00을 의미하고, 특정 값은 NULL, b는 바이트로 표현된다.

def pad(data):
    
    return data + b"\x00" * (16 - len(data) % 16)


# 이미지 데이터를 RGB에 매핑한다.

def trans_format_RGB(data):
    
    red, green, blue = tuple(map(lambda e: [data[i] for i in range(0, len(data)) if i % 3 == e], [0, 1, 2]))

    pixels = tuple(zip(red, green, blue))

    return pixels


def decrypt_image_ecb(filename):
    
    # bmp 확장자를 가지고 있는 그림을 열어서 RGB 이미지로 변환한다.
    im = Image.open(filename)

    # 이미지의 데이터를 픽셀 바이트 값으로 변환한다.
    value_vector = im.convert("RGB").tobytes()

    imlength = len(value_vector)

    # 암호화가 되어 있거나 텍스트 공간에 채워져 있는 데이터의 픽셀 값을 매핑시킨다.
    value_encrypt = trans_format_RGB(aes_ecb_decrypt(key, pad(value_vector))[:imlength])

    # 새로운 객체를 생성하고 해당 데이터를 저장한다.
    im2 = Image.new(im.mode, im.size)
    im2.putdata(value_encrypt)

    # filename_encrypted_ecb를 bmp 확장자로 저장한다.
    im2.save(filename_decrypted_ecb + "." + format, format)


# ECB 암호화(기본 모드는 ECB 암호화를 사용함.)

def aes_ecb_decrypt(key, data, mode=AES.MODE_ECB):
    
    aes = AES.new(key, mode)
    new_data = aes.decrypt(data)

    return new_data

key = 'iefdkf2435434111'; # key string = 16으로 맞춰준다.
# key = key_generator(16)

# 이미지 암호화를 실행하고, 해당 디렉토리에서 암호화된 이미지를 생성한다. (ecb 진행)
decrypt_image_ecb(filename)

# 이미지 암호화를 실행하고, 해당 디렉토리에서 암호화된 이미지를 생성한다. (cbc 진행)

cv2.imread(filename) # 원본 이미지 열기
cv2.imread('image_decrypted_ecb.png') # ecb 암호화가 진행된 이미지 열기
