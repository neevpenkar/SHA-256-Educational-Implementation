from SHAFunctions import *

test = "532eaabd9574880dbf76b9b8cc00832c20a6ec113d682299550d7a6e0f345e25"
temp = b"Test"
h = SHA256Hash(temp)
print(h.hex() == test)