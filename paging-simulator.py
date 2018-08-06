from collections import defaultdict
import time


def hex2bin(hexdata):
    scale = 16
    num_of_bits = 8
    b = bin(int(hexdata, scale))[2:].zfill(num_of_bits)
    return b


def read_file(page_size, path_file):
    d = {}
    count = 0
    with open(path_file) as f:
        for line in f:
            (key, val) = line.split()
            d[count] = (hex2bin(key)[:page_size])
            count += 1
    return d


def hash_file(page_size, path_file):
    d = defaultdict(list)
    # a = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2]
    a = read_file(page_size, path_file)
    for idx, value in enumerate(a):
        d[value].append(idx)

    return d


def predict(frames, process_list, idx):
    res = -1
    farthest = idx
    for i, fr in enumerate(frames):
        j = 0
        for j in range(idx, len(process_list)):
            if frames[i] == process_list[j]:
                if j > farthest:
                    farthest = j
                    res = i
                break
        if j == len(process_list) - 1:
            return i

    return res if res != -1 else 0


def optimal(process_list, frames_size):
    frames = []
    hits = 0
    misses = 0
    for idx, page in process_list.items():
        if page in frames:
            hits += 1
            continue

        if len(frames) < frames_size:
            frames.append(page)
            misses += 1

        else:
            replace = predict(frames, process_list, idx + 1)
            frames[replace] = page
            misses += 1

    print('n hits = %s' % hits)
    print('n misses = %s' % misses)


def aprox_lru(process_list, frames_size):
    frames = []
    reference_bytes = [0] * frames_size
    hits = 0
    misses = 0
    for idx, page in process_list.items():

        if page in frames:
            hits += 1
            reference_bytes[frames.index(page)] = 1
            continue

        if len(frames) < frames_size:
            frames.append(page)
            misses += 1

        else:
            replace = reference_bytes.index(min(reference_bytes))
            frames[replace] = page
            misses += 1

    print('n hits = %s' % hits)
    print('n misses = %s' % misses)


# frames = int(input("Numero de frames: "))
# page_size = int(input("Tamanho da página: "))
frames_size = 8
page_size = 16

start_time = time.time()
process_list = read_file(page_size, '/home/medina/paging-simulator/traces/gcc.trace')
# processList = { 0:7, 1:0, 2:1, 3:2, 4:0, 5:3, 6:0, 7:4, 8:2, 9:3, 10:0, 11:3, 12:2 }
# processList = hash_file(page_size, '/home/medina/UNIOESTE/SO/traces/gcc.trace')

print("--------------------Algoritmo Otimo-----------------------")
optimal(process_list, frames_size)
print("--------------------LRU Aproximado-----------------------")
aprox_lru(process_list, frames_size)

exec_time = (time.time() - start_time)
if exec_time > 60:
    print("--- Execução: %s minutos ---" % (exec_time / 60))
else:
    print("--- Execução: %s segundos ---" % exec_time)
