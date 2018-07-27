import time

def hex2bin(hexdata):
    scale = 16 
    num_of_bits = 8
    b = bin(int(hexdata, scale))[2:].zfill(num_of_bits)
    return b

def readFile(page_size):
    d = []
    with open('/home/medina/UNIOESTE/SO/traces/gcc.trace') as f:
        for line in f:
            (key, val) = line.split()
            d.append(hex2bin(key)[:page_size])
    return d

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
    for idx, page in enumerate(processList):
        if page in frames:
            hits += 1
            continue

        if len(frames) < frames_size:
            frames.append(page)

        else:
            replace = predict(frames, processList, idx + 1)
            frames[replace] = page

    print('n hits = ' + str(hits))
    print('n misses = ' + str(len(processList) - hits))            

# frames = int(input())
# page_size = int(input())
frames_size = 4
page_size = 16

start_time = time.time()
processList = readFile(page_size)
optimal(processList, frames_size)
print("--- %s seconds ---" % (time.time() - start_time))
