# import main as mn
from threading import Thread
from whatsapp_client import main as client
import sys
import random
import string


def gen_input(output="test.txt", num_lines=5):
	f = open(output, "w")
	for i in range(num_lines):
		# choice = random.randint(0, 100)
		choice = 0
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
	if sys.stdin.isatty():
		exit()
	input_file = "input.txt"
	output_file = "output.txt"
	num_of_lines = 15

	gen_input(input_file, num_of_lines)
	sys.stdin = open(input_file)
	sys.stdout = open(output_file, "w")

	client()

	sys.stdin = sys.__stdin__
	sys.stdout = sys.__stdout__

	f1 = open(output_file, "r")
	last_line = f1.readlines()[-10]
	f1.close()
	x = last_line.count(", ") + 1
	print(str(x) + " from " + str(num_of_lines))
	print("ratio: " + str(x / num_of_lines))
	last_line = last_line.split("\'], [\'")
	last_line[0] = last_line[0][3:]
	last_line[len(last_line) - 1] = last_line[len(last_line) - 1][:-4]
	for line in last_line:
		print(line)
	# servers.join(50)
