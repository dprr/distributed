import random
import functools
import binascii
import shamir
from constants import *


_rint = functools.partial(random.SystemRandom().randint, 0)


def __make_msg_secret_shares(msg, minimum, shares, prime=PRIME_SSSS):
	"""
	:param msg: the msg to hide
	:param minimum: how many points needs to recover the msg
	:param shares: how many points will be crate
	:return: Generates a shamir pool, returns
	the secret and the share points. as tuple (secret, share points)
	"""
	if minimum > shares:
		raise ValueError("pool secret would be irrecoverable")
	poly = [_rint(prime) for i in range(minimum)]
	poly[0] = str_to_int(msg)
	points = [(i, shamir._eval_at(poly, i, prime)) for i in range(1, shares + 1)]
	return poly[0], points


def str_to_int(msg_str):
	"""
	:param msg_str: the msg
	:return: msg as int
	"""
	if msg_str != "":
		msg_int = int(binascii.hexlify(msg_str.encode("utf-8")), 16)
	else:
		msg_int = 0
	return msg_int


def int_to_str(msg_int):
	"""
	:param msg_int: msg as int
	:return: the msg
	"""
	if msg_int == 0:
		return ""
	try:
		msg_str = binascii.unhexlify(hex(msg_int)[2:]).decode("utf-8")
		return msg_str
	except:
		return "Not ciphertext of utf-8"


def generate_secret_from_msg(msg, req, total):
	"""
	:param msg: the msg to hide
	:param req: how many points need to recover the msg
	:param total: how many point to create
	:return: points to send to servers
	"""
	secret, points = __make_msg_secret_shares(msg, req, total)
	if len(msg) > MAX_MSG_LEN:
		errmsg = "msg can't be recovered, the msg is too long.\n" \
				 "max len is " + MAX_MSG_LEN + " chars, your msg len is " + str(len(msg)) + " chars"
		raise ValueError(errmsg)
	if msg != int_to_str(shamir.recover_secret(points, PRIME_SSSS)):
		errmsg = "msg can't be recovered, for unknown reason, please contact us"
		raise ValueError(errmsg)
	return points


def recover_secret(shares):
	"""
	:param shares: list of points as following: [(server number, server number),...,(server number, server number)]
	:return: the msg as int. this function doesn't check if the msg is valid.
	"""
	return shamir.recover_secret(shares, PRIME_SSSS)


def run():
	"""
	demo of this lib
	"""
	msg = ""
	print(len(msg))
	points = generate_secret_from_msg(msg, 2, 4)
	for point in points:
		print(point)

	print(int_to_str(recover_secret([points[0], points[3], points[2]])))


if __name__ == "__main__":
	run()
