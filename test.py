import main as mn
from whatsapp_client import main as client
from threading import Thread
import sys
import random
import string


def gen_input(output="test.txt", num_lines=5):
	f = open(output, "w")
	for i in range(num_lines):
		choice = random.randint(0, 100)
		if choice < 80:
			print("s", file=f)
			message = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(30))
			print(message, file=f)
		elif choice < 90:
			print("r", file=f)
		else:
			print("d", file=f)
	print("d", file=f)
	print("q", file=f)
	f.close()


if __name__ == '__main__':
	# servers = Thread(target=mn.run_servers())
	# servers.start()
	input_file = "input.txt"
	output_file = "output.txt"
	gen_input(input_file, 50)
	# if not sys.stdin.isatty():
	# 	sys.stdin = open(input_file)
	# 	sys.stdout = open(output_file, "w")
	# 	client()
	# 	sys.stdin = sys.__stdin__
	# 	sys.stdout = sys.__stdout__
	# servers.join(50)
