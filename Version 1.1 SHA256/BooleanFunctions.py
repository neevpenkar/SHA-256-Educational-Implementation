from bitarray import bitarray

def shiftRight(word, times = 1):
    number = int.from_bytes(word) >> times
    return bytearray(number.to_bytes(4, 'big'))

def printWord(word):
    for i in word:
        print(bin(i), end=" ")
    print()

def toInt(bitArr):
    i = 0
    s = 0
    bitArr.reverse()
    for bit in bitArr:
        s += bit * pow(2, i)
        i += 1
    return s

def shiftRight(word: bitarray, times=1):
    if len(word) != 32:
        print("Error: Non 32 bit word")
        print(word, len(word))
        exit(-2)
    return word.copy() >> (times % 32)

def shiftLeft(word: bitarray, times=1):
    if len(word) != 32:
        print("Error: Non 32 bit word")
        exit(-2)
    return word.copy() << (times % 32)

def rotateRight(word: bitarray, times=1):
    times %= 32

    temp1 = shiftRight(word, times)
    temp2 = shiftLeft(word, 32 - times)

    return temp1 | temp2

def Addition_1(arr1: bitarray, arr2: bitarray):
    a = int.from_bytes(arr1.tobytes(), byteorder='big')
    b = int.from_bytes(arr2.tobytes(), byteorder='big')

    c = int(a + b) % 2**32
    temp = bitarray()
    temp.frombytes(c.to_bytes(4, byteorder='big'))
    return temp

def Addition(arr1, arr2, arr3, arr4):
    return Addition_1(Addition_1(arr1, arr2), Addition_1(arr3, arr4))
