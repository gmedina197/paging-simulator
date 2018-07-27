import time
from collections import defaultdict

def hex2bin(hexdata):
    scale = 16 
    num_of_bits = 8
    b = bin(int(hexdata, scale))[2:].zfill(num_of_bits)
    return b

def readFile(page_size, path_file):
    d = {}
    count = 1
    with open(path_file) as f:
        for line in f:
            (key, val) = line.split()
            d[count] = hex2bin(key)[:page_size]
            count += 1
    return d

def hashFile(page_size, path_file):
    d = defaultdict(list)
    a = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2]

    for idx, value in enumerate(a):
        d[value].append(idx)

    print(d.items())

def predict(frames, processList, idx):
    res = -1
    farthest = idx
    for i, fr in enumerate(frames):
        j = 0
        for j in range(idx, len(processList)):
            if frames[i] == processList[j]:
                if j > farthest:
                    farthest = j
                    res = i
                break
        if j == len(processList) - 1:
            return i

    return res if res != -1 else 0

def optimal(processList, frames_size):
    frames = []
    hits = 0
    misses = 0
    for idx, page in processList.items():
        if page in frames:
            hits += 1
            continue

        if len(frames) < frames_size:
            frames.append(page)
            misses += 1

        else:
            replace = predict(frames, processList, idx + 1)
            frames[replace] = page
            misses += 1
        
    print('n hits = %s' % hits)
    print('n misses = %s' % misses) 

def aprox_LRU(processList, frames_size):
    pass

#frames = int(input("Numero de frames: "))
#page_size = int(input("Tamanho da página: "))
frames_size = 4
page_size = 16

start_time = time.time()
#processList = readFile(page_size, '/home/medina/UNIOESTE/SO/traces/gcc.trace')
processList = { 0:7, 1:0, 2:1, 3:2, 4:0, 5:3, 6:0, 7:4, 8:2, 9:3, 10:0, 11:3, 12:2 }
hashFile(page_size, '/home/medina/UNIOESTE/SO/traces/gcc.trace')

""" print("--------------------Algoritmo Otimo-----------------------")
optimal(processList, frames_size)
print("--------------------LRU Aproximado-----------------------")
aprox_LRU(processList, frames_size)

exec_time = (time.time() - start_time)
if exec_time > 60:
    print("---Execução: %s minutos ---" % ( exec_time / 60))
else:
    print("---Execução: %s segundos ---" % exec_time) """

