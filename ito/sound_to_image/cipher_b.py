from PIL import Image
import wave
from scipy import fromstring, int16
import math

FRAME_RATE = 44100
input_name = "input.wav"
output_name = "output.tmp"


def input_wave():
    global input_name
    input_name = input("input_file->")
    sound = wave.open(input_name)
    return sound


def print_info(sound):
    print("チャンネル数:", sound.getnchannels())
    print("サンプル幅:", sound.getsampwidth())
    print("サンプリング周波数:", sound.getframerate())
    print("フレーム数:", sound.getnframes())
    print("パラメータ:", sound.getparams())
    print("長さ（秒）:", float(sound.getnframes()) / sound.getframerate())


def get_data(sound):
    buffer = sound.readframes(sound.getnframes())
    buffer = fromstring(buffer, dtype=int16)
    data_a = []
    data_b = []
    channels = sound.getnchannels()
    print(len(buffer))
    for i in buffer:
        tmp = 32768+i
        a1 = tmp // 256
        a2 = a1
        a1 = a1 // 16
        a2 = a2 % 16
        b1 = tmp % 256
        b2 = b1
        b1 = b1 // 16
        b2 = b2 % 16
        data_a.append(a1*16+b1)
        data_b.append(a2*16+b2)
    data = [data_a, data_b, channels]
    return data


def make_cip(data):
    size = []
    size.append(int(math.sqrt(len(data[0])))+1)
    size.append(size[0])
    print(size)
    new_a = Image.new("RGB", size)
    new_b = Image.new("RGB", size)
    i = 0
    for x in range(0, size[0]):
        for y in range(size[1]):
            if x == 0 and y == 0:
                new_a.putpixel((x, y), (0, 0, 0))
                new_b.putpixel((x, y), (255, 255, 255))
            elif x == 1 and y == 0:
                new_a.putpixel((x, y), (data[2], data[2], data[2]))
                new_b.putpixel((x, y), (data[2], data[2], data[2]))
            elif i < len(data[0]):
                a = data[0][i]
                b = data[1][i]
                new_a.putpixel((x, y), (a, a, a))
                new_b.putpixel((x, y), (b, b, b))
            i += 1
    new_a.save("a.bmp")
    new_b.save("b.bmp")
    return 0


if __name__ == "__main__":
    s = input_wave()
    print_info(s)
    make_cip(get_data(s))
