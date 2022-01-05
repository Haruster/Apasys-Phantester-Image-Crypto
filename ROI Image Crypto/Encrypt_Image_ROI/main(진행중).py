
import random
import string
import cv2
from Crypto.Cipher import AES
from PIL import Image
from tensorflow import keras

image_data = cv2.imread('image.jpg')
filename_encrypted_ecb = "image_encrypted_ecb"
filename_encrypted_cbc = "image_encrypted_cbc"
format = "bmp"

key = key_generator(16)

x = 460
y = 295
w = 100
h = 100

ROI = image_data[y : y + h, x : x + w]

print(ROI.shape)

cv2.rectangle(ROI, (0, 0), (h - 1, w - 1), (0, 255, 0))

# key_genarator 함수는 소문자 16개의 문자열을 임의로 생성한다.
def key_generator(size = 16, chars = string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))


# AES 암호화의 텍스트 공간은 16개의 정수 배수로 균등하게 나눌 수 없으므로 이를 채워야하며,
# 해당 아스키코드(ASCII)에서 "\x00"은 0x00을 의미하고, 특정 값은 NULL, b는 바이트로 표현된다.
def pad(data):
    return data + b"\x00" * (16 - len(data) % 16)


# 이미지 데이터를 RGB에 매핑한다.
def trans_format_RGB(data):
    red, green, blue = tuple(map(lambda e: [data[i] for i in range(0, len(data)) if i % 3 == e], [0, 1, 2]))

    pixels = tuple(zip(red, green, blue))

    return pixels


def encrypt_image_ecb(image_data):
    # bmp 확장자를 가지고 있는 그림을 열어서 RGB 이미지로 변환한다.
    im = Image.open(image_data)

    # 이미지의 데이터를 픽셀 바이트 값으로 변환한다.
    value_vector = im.convert("RGB").tobytes()

    imlength = len(value_vector)

    # 암호화가 되어 있거나 텍스트 공간에 채워져 있는 데이터의 픽셀 값을 매핑시킨다.
    value_encrypt = trans_format_RGB(aes_ecb_encrypt(key, pad(value_vector))[:imlength])

    # 새로운 객체를 생성하고 해당 데이터를 저장한다.
    im2 = Image.new(im.mode, im.size)
    im2.putdata(value_encrypt)

    # filename_encrypted_ecb를 bmp 확장자로 저장한다.
    im2.save(filename_encrypted_ecb + "." + format, format)

def encrypt_image_cbc(image_data):
    
    # bmp 확장자를 가지고 있는 그림을 열어서 RGB 이미지로 변환한다.
    im = Image.open(image_data)
    value_vector = im.convert("RGB").tobytes()

    # 이미지의 데이터를 픽셀 바이트 값으로 변환한다.
    imlength = len(value_vector)

    # 작성되거나 암호화 되어 있는 데이터에 대해서 픽셀 값을 매핑시킨다.
    value_encrypt = trans_format_RGB(aes_cbc_encrypt(key, pad(value_vector))[:imlength])

    # 새로운 객체를 생성하고 해당 데이터를 저장한다.
    im2 = Image.new(im.mode, im.size)
    im2.putdata(value_encrypt)

    # file_name_encrypted_cbc를 bmp 확장자로 저장한다.
    im2.save(filename_encrypted_cbc + "." + format, format)


# ECB 암호화(기본 모드는 ECB 암호화를 사용함.)

def aes_ecb_encrypt(key, data, mode=AES.MODE_ECB):
    
    aes = AES.new(key, mode)
    new_data = aes.encrypt(data)
    
    return new_data

# CBC 암호화

def aes_cbc_encrypt(key, data, mode=AES.MODE_CBC):
    
    # Random_IV는 임의의 값을 나타낸다.
    Random_IV = key_generator(16)
    aes = AES.new(key, mode, Random_IV)
    new_data = aes.encrypt(data)
    
    return new_data

cv2.imshow('img', image_data)
cv2.waitKey(0)
cv2.destroyAllWindows()
