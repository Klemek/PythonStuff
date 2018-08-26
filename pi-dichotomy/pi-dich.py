import os.path
import math


def tryparse_int(value):
    try:
        return int(value)
    except ValueError:
        return None


def do_dich(name):
    pi = load(name)
    b = "0110"
    x = 14
    d = 25
    n = 3
    while n < len(pi):
        if x > d:
            x -= d
            b += "1"
        else:
            b += "0"
        x = 10 * x + int(str(pi[n]))
        d *= 5
        n += 1
    return b


def load(name):
    d = ""
    with open(name) as f:
        for line in f:
            d = line.strip()
            break
    return d


def save(name, bi):
    with open(name, mode='w') as f:
        f.write(bi)


def verify_dich(b):
    x = 4.0
    n = float(0)
    i = 0
    while i < len(b) and x > 0:
        if b[i] == '1':
            n += x
        x /= 2.0
        i += 1
    print(n)
    return n == 3.141592653589793


def save_byte(name, data):
    with open(name, mode='wb') as f:
        f.write(bytearray(data))


def get_int(b):
    return int((b * 8)[:8], 2)


def n2b(num, nbyte=4):
    b = []
    for i in range(nbyte):
        b += [num % 256]
        num //= 256
    return b


def print_bytes(data):
    for i in range(len(data) // 16 + 1):
        for j in range(16):
            if i * 16 + j >= len(data):
                print(" . ", end='')
            else:
                print("{:02x} ".format(data[i * 16 + j]), end='')
        print()


def save_bmp(name, data, width):
    # fix data size
    height = len(data) // (width * 3)
    if len(data) > height * width * 3:
        data = data[0:height * width * 3]

    # fix line width not %4
    line_width = (width * 3) % 4
    if line_width != 0:
        tail = (3 - line_width) * [0] + [255]
        data2 = []
        for i in range(height):
            data2 += data[i * width * 3:(i + 1) * width * 3] + tail
        data = data2

    header = [0] * 54
    header[0:2] = [66, 77]  # BM
    header[2:6] = n2b(len(data) + 54)  # file size
    # 4 bytes application reserved
    header[10:14] = n2b(54)  # offset of data
    header[14:18] = n2b(40)  # size of header
    header[18:22] = n2b(width)  # width
    header[22:26] = n2b(height)  # height
    header[26:28] = n2b(1, 2)  # color panes
    header[28:30] = n2b(24, 2)  # color depth
    # 4 bytes compression method
    # 4 bytes optional image size
    header[38:42] = n2b(3780)  # horizontal resolution
    header[42:46] = n2b(3780)  # vertical resolution
    # 4 bytes number of colors
    # 4 bytes number of important colors

    print_bytes(header)
    with open(name, mode='wb') as f:
        f.write(bytearray(header + data))


def save_wav(name, data, channels, freq, sampling):
    header_size = 44
    header = [0] * header_size

    bytesPerBloc = int(channels * sampling / 8)
    dataSize = len(data)
    mod = dataSize % bytesPerBloc
    if mod > 0:
        dataSize -= mod

    # file info
    header[0:4] = [0x52, 0x49, 0x46, 0x46]  # "RIFF"
    header[4:8] = n2b(header_size + dataSize - 8)  # file size - 8bytes
    header[8:12] = [0x57, 0x41, 0x56, 0x45]  # "WAVE"
    # audio format
    header[12:16] = [0x66, 0x6D, 0x74, 0x20]
    header[16:20] = n2b(16)
    header[20:22] = n2b(1)  # PCM format
    header[22:24] = n2b(channels)  # nb of channels
    header[24:28] = n2b(freq)  # frequency 11025, 22050, 44100, 48000, 96000
    header[28:32] = n2b(freq * bytesPerBloc)  # BytePerSec
    header[32:34] = n2b(bytesPerBloc)  # BytePerBloc
    header[34:36] = n2b(sampling)  # BitsPerSample 8, 16, 24
    # data
    header[36:40] = [0x64, 0x61, 0x74, 0x61]  # "data"
    header[40:44] = n2b(dataSize)

    print_bytes(header)
    with open(name, mode='wb') as f:
        f.write(bytearray(header + data[:dataSize]))


def get_data(b):
    return [int(b[n * 8:(n + 1) * 8], 2) for n in range(int(len(b) / 8))]


def get_bw_bmp_data(b, width):
    return get_grey_bmp_data(b, width, 1)


def get_grey_bmp_data(b, width, l):
    data = []
    for n in range(width * width):
        c = get_int(b[n * l:(n + 1) * l])
        data += [c, c, c]  # grey
    return data


def get_color_bmp_data(b, width, l):
    data = []
    for n in range(int(width * width)):
        c1 = get_int(b[(3 * n) * l:(3 * n + 1) * l])
        c2 = get_int(b[(3 * n + 1) * l:(3 * n + 2) * l])
        c3 = get_int(b[(3 * n + 2) * l:(3 * n + 3) * l])
        data += [c1, c2, c3]  # grey
    return data


def main():
    DIGIT_FILE = "pi1000000.txt"
    BIN_FILE = "pi1000000bin.txt"
    bpi = ""
    if os.path.isfile(BIN_FILE):
        print("loading dichotomy...")
        bpi = load(BIN_FILE)
    elif os.path.isfile(DIGIT_FILE):
        print("computing dichotomy (this might take a while)...")
        bpi = do_dich(DIGIT_FILE)
        print("saving dichotomy...")
        save(BIN_FILE, bpi)
    else:
        print(DIGIT_FILE, "was not found")
        exit(1)
    print(len(bpi), "bits of dichotomy in memory")
    print()
    print("verifying dichotomy...")
    if not (verify_dich(bpi)):
        print("could not verify dichotomy you may delete the file ", BIN_FILE)
        exit(1)
    print()
    print("modes :")
    print("1:binary file")
    print("2:black & white bitmap file")
    print("3:grey scale bitmap file")
    print("4:color scale bitmap file")
    print("5:wave file")
    mode = tryparse_int(input("select a mode : "))
    print()
    if mode == 1:
        defname = "pi_bin"
        name = input("enter file name : [{}] ".format(defname)).strip()
        if len(name) == 0:
            name = defname
        print("getting data...")
        data = get_data(bpi)
        print("saving to file '" + name + "' ...")
        save_byte(name, data)
        print("saved to file '" + name + "'")
    elif mode == 2:
        maxw = int(math.sqrt(len(bpi)))
        width = tryparse_int(input("enter image width (max:{0}): [{0}] ".format(maxw)))
        if width is None or width > maxw or width < 1:
            width = maxw
        defname = "pi_bw_{}.bmp".format(width)
        name = input("enter file name : [{}] ".format(defname)).strip()
        if len(name) == 0:
            name = defname
        if not (name.endswith(".bmp")):
            name += ".bmp"
        print("getting data...")
        data = get_bw_bmp_data(bpi, width)
        print("saving to file '" + name + "' ...")
        save_bmp(name, data, width)
        print("saved to file '" + name + "'")
    elif mode == 3:
        l = tryparse_int(input("enter grey depth (max:8): [8] "))
        if l is None or l > 8:
            l = 8
        if l < 1:
            l = 1
        maxw = int(math.sqrt(len(bpi)) / l)
        width = tryparse_int(input("enter image width (max:{0}): [{0}] ".format(maxw)))
        if width is None or width > maxw or width < 1:
            width = maxw
        defname = "pi_grey_{}_{}.bmp".format(l, width)
        name = input("enter file name : [{}] ".format(defname)).strip()
        if len(name) == 0:
            name = defname
        if not (name.endswith(".bmp")):
            name += ".bmp"
        print("getting data...")
        data = get_grey_bmp_data(bpi, width, l)
        print("saving to file '" + name + "' ...")
        save_bmp(name, data, width)
        print("saved to file '" + name + "'")
    elif mode == 4:
        l = tryparse_int(input("enter color depth (max:8): [8] "))
        if l is None or l > 8:
            l = 8
        if l < 1:
            l = 1
        maxw = int(math.sqrt(len(bpi)) / (l * 3))
        width = tryparse_int(input("enter image width (max:{0}): [{0}] ".format(maxw)))
        if width is None or width > maxw or width < 1:
            width = maxw
        defname = "pi_color_{}_{}.bmp".format(l, width)
        name = input("enter file name : [{}] ".format(defname)).strip()
        if len(name) == 0:
            name = defname
        if not (name.endswith(".bmp")):
            name += ".bmp"
        print("getting data...")
        data = get_color_bmp_data(bpi, width, l)
        print("saving to file '" + name + "' ...")
        save_bmp(name, data, width)
        print("saved to file '" + name + "'")
    elif mode == 5:
        channels = tryparse_int(input("number of channels (max:6) : [1] "))
        if channels is None or channels <= 0:
            channels = 1
        if channels > 6:
            channels = 6
        freq = tryparse_int(input("frequency (1->11k, 2->22k, 3->44.1k, 4->48k 5->96k) : [3] "))
        if freq is None:
            freq = 3
        if freq <= 0:
            freq = 1
        if freq > 5:
            freq = 5
        freq = int(11025 * math.pow(2, freq - 1))
        bps = tryparse_int(input("bits per sample (1->8, 2->16, 3->24) : [1] "))
        if bps is None or bps <= 0:
            bps = 1
        if bps > 3:
            bps = 6
        bps *= 8
        defname = "pi_{}_{}_{}.wav".format(channels, bps, int(freq / 1000))
        name = input("enter file name : [{}] ".format(defname)).strip()
        if len(name) == 0:
            name = defname
        if not (name.endswith(".wav")):
            name += ".wav"
        print("getting data...")
        data = get_data(bpi)
        print("saving to file '" + name + "' ...")
        save_wav(name, data, channels, freq, bps)
        print("saved to file '" + name + "'")
    print()
    print("goodbye")


main()
