import main as mn
from whatsapp_client import main as client

import threading
import sys
import random
import string


def gen_test(num_lines=5):
	f = open("test.txt", "w")
	for i in range(num_lines):
		choice = random.randint(0, 100)
		if choice < 80:
			print("s", file=f)
			message = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(30))
			print(message, file=f)
		elif choice < 90:
			print("r", file=f)
		else:
			print("d", file=f)
	print("d", file=f)
	print("q", file=f)
	f.close()


class Tee(object):
	def __init__(self, input_handle, output_handle):
		self.input = input_handle
		self.output = output_handle

	def readline(self):
		result = self.input.readline()
		self.output.write(result)

		return result


if __name__ == '__main__':
	gen_test(50)
	f = open("test.txt")
	if not sys.stdin.isatty():
		sys.stdin = Tee(input_handle=f, output_handle=sys.stdout)
		client()
	sys.stdin = sys.__stdin__


# sys.stdin = redirected_input(sys.stdin,
# s = StringIO.StringIO('Hello, world!')
# >>> sys.stdin = s ; r = raw_input('What you say?\n') ; sys.stdin = sys.__stdin__