PRIME_shamir = 2**127 - 1
PRIME_SSSS = 2**4423 - 1
MAX_MSG_LEN = 553
LEN_OF_BOARD = 10
# TODO: change the vector size
SIZE = 10
messagesVec = [0] * SIZE

EPOCH = 10
SERVER_PORTS = [i for i in range(10000, 10004)]
CLIENT_PORTS = [i for i in range(20000, 20010)]
local_host = "127.0.0.1"

def int_to_bytes(x):
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')


def int_from_bytes(xbytes):
    return int.from_bytes(xbytes, 'big')
