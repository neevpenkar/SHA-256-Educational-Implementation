from BooleanFunctions import *

K = [0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
    0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
    0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
    0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
    0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
    0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
    0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,
    0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2]

initialHashes = [0x6a09e667,0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 
                 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]

def convertInt2BitArray(number: int):
    temp = bitarray()
    temp.frombytes(number.to_bytes(4, 'big'))
    return temp

def Ch(x, y, z):
    return (x & y) ^ ((~x) & z)

def Maj(x, y, z):
    return (x & y) ^ (x & z) ^ (y & z)

def SIGMA0(x):
    return rotateRight(x, 2) ^ rotateRight(x, 13) ^ rotateRight(x, 22)

def SIGMA1(x):
    return rotateRight(x, 6) ^ rotateRight(x, 11) ^ rotateRight(x, 25)

def sigma0(x):
    return rotateRight(x,7) ^ rotateRight(x, 18) ^ shiftRight(x, 3)

def sigma1(x):
    return rotateRight(x, 17) ^ rotateRight(x, 19) ^ shiftRight(x, 10)

# Block Decomposition

# The following function will generate the first 16 blocks of the words array
# In essence break down the 512 bit block into 16 words of 32 bits
def splitBlock(block: bitarray):
    words_list = []

    for row in range(16):
        temp = bitarray(32) 
        for col in range(32):
            temp [col] = block[32 * row + col]
        words_list.append(temp)

    return words_list

# This function contains the "Block Decomposition" algorithm described in the spec
# Make the first 16 words and from them make the remaining 48 words
def splitBlockIntoWords(block: bitarray):
    if len(block) != 512:
        print("Error: Block size not 512 bits")
        exit(-3)
        return

    words = splitBlock(block)

    for i in range(16, 64):
        temp = bitarray()
        temp = Addition(sigma1(words[i-2]) , words[i-7], sigma0(words[i-15]), words[i-16])
        words.append(temp)

    # This function will return the array/list of 64 words which will be used for compression
    return words


# The heart and soul of SHA 2
# This function will take in the last message block's partial hashes as well as the current message
# block and will compress the block into half its size - Compress 512 bit block to 8 partial hashes
# each 32 bit long. The result of these hashes will be added* onto the previous hashes
# * - Modulo 2**32 addition
def compressionFunction(words, previous_Hashes):

    a = previous_Hashes[0].copy()
    b = previous_Hashes[1].copy()
    c = previous_Hashes[2].copy()
    d = previous_Hashes[3].copy()

    e = previous_Hashes[4].copy()
    f = previous_Hashes[5].copy()
    g = previous_Hashes[6].copy()
    h = previous_Hashes[7].copy()

    for i in range(64):
        T1 = Addition_1(Addition(h, SIGMA1(e), Ch(e,f,g), convertInt2BitArray(K[i])), words[i])
        T2 = Addition_1(SIGMA0(a), Maj(a, b, c))
        
        # Problems start with i = 16 (15)
        # word at index 15 does not have one 1
        #print(i, words[i])

        h = g.copy()
        g = f.copy()
        f = e.copy()
        e = Addition_1(d, T1)
        d = c.copy()
        c = b.copy()
        b = a.copy()
        a = Addition_1(T1, T2)

    previous_Hashes[0] = Addition_1(previous_Hashes[0], a)
    previous_Hashes[1] = Addition_1(previous_Hashes[1], b)
    previous_Hashes[2] = Addition_1(previous_Hashes[2], c)
    previous_Hashes[3] = Addition_1(previous_Hashes[3], d)

    previous_Hashes[4] = Addition_1(previous_Hashes[4], e)
    previous_Hashes[5] = Addition_1(previous_Hashes[5], f)
    previous_Hashes[6] = Addition_1(previous_Hashes[6], g)
    previous_Hashes[7] = Addition_1(previous_Hashes[7], h)

    return previous_Hashes

# This function will take in a the block of message, split it and perform the compression function
# This function will also init the initial hash values as described in the spec
def processBlock(block: bitarray):
    if len(block) != 512:
        print("Error Block Not 512 bits")
        exit(-1)
    
    initHashes = []
    for i in initialHashes:
        initHashes.append(convertInt2BitArray(i))

    words = splitBlockIntoWords(block)
    hashes = compressionFunction(words, initHashes)

    # Combine the hashes and return as bytes
    finalHash = bitarray()
    for i in hashes:
        finalHash += i

    return finalHash.tobytes()

# Padding Function: will pad the message according to the spec
def padBlock_SHA(raw_bytes: bytearray):
    if raw_bytes == b"":
        block = bitarray('1' + '0'*511)
    else:
        # Convert from more common bytearray to bitarray
        raw_block = bitarray(endian='big')
        raw_block.frombytes(raw_bytes)
        L = len(raw_block)

        # Append "1" to the end of the message
        block = raw_block + '1'

        # Example for N=1: Append '0' to the block till length is 448
        while (len(block) + 1) % 512 != 448:
            block += '0'

        # Append the length of the original message
        # Make sure that the space take for the length is 64 bits

        temp = bitarray()
        temp.frombytes(L.to_bytes())
        while len(temp) <= 64:
            temp.insert(0,0)

        block += temp

        # Clear Block Memory
        temp.clear()
        L = 0

    return block

def SHA256Hash(message: bytearray):
    ''' As of now, this algorithm can only process one block of data, after padding'''

    # Pad Block
    padded = padBlock_SHA(message)

    # Return Hashed Data
    return processBlock(padded)