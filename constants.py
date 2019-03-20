PRIME = 2 ** 4423 - 1

MAX_MSG_LEN = 553
LEN_OF_BOARD = 10
SIZE_OF_MSG = 1024*1024

EPOCH = 10
SERVER_PORTS = [i for i in range(10000, 10004)]
local_host = "127.0.0.1"

def int_to_bytes(x):
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')


def int_from_bytes(xbytes):
    return int.from_bytes(xbytes, 'big')
