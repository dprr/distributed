# from __future__ import division
import random
import functools
import binascii
import shamir


_PRIME = 2**8191 - 1

_rint = functools.partial(random.SystemRandom().randint, 0)

def make_msg_secret_shares(msg, minimum, shares, prime=_PRIME):
    '''
    Generates a shamir pool, returns
    the secret and the share points.
    '''
    if minimum > shares:
        raise ValueError("pool secret would be irrecoverable")
    poly = [_rint(prime) for i in range(minimum)]
    poly[0] = str_to_int(msg)
    points = [(i, shamir._eval_at(poly, i, prime))
              for i in range(1, shares + 1)]
    return poly[0], points


def str_to_int(msg_str):
	'''
	:return: msg as int
	'''
	if msg_str != "":
		msg_int = int(binascii.hexlify(msg_str.encode("utf-8")), 16)
	else:
		msg_int = 0
	return msg_int


def int_to_str(msg_int):
	if msg_int == 0:
		return ""
	try:
		msg_str = binascii.unhexlify(hex(msg_int)[2:]).decode("utf-8")
		return msg_str
	except:
		return "Not ciphertext of utf-8"


def generate_secret_from_msg(msg, req, total):
	secret, points = make_msg_secret_shares(msg, req, total)
	if msg != int_to_str(shamir.recover_secret(points, _PRIME)):
		raise ValueError("msg can't recover, probably the msg too long")
	return points


def recover_secret(shares):
	return int_to_str(shamir.recover_secret(shares, _PRIME))


def run():
	msg = ""
	points = generate_secret_from_msg(msg, 3, 4)
	for point in points:
		print(point)

	print(recover_secret([points[0], points[3], points[2]]))

if __name__ == "__main__":
	run()
