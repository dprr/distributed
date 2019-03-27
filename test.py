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
			message = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(30))
			print(message, file=f)
		elif choice < 90:
			print("r", file=f)
		else:
			print("d", file=f)
	print("d", file=f)
	print("d", file=f)
	print("q", file=f)
	f.close()


def run_client(input_file="input.txt", output_file="output.txt"):
	# if sys.stdin.isatty():
	# 	exit()
	print(output_file)
	num_of_lines = 5
	if input_file != sys.__stdin__:
		gen_input(input_file, num_of_lines)
		sys.stdin = open(input_file)
	# if output_file != sys.__stdout__:
	# 	sys.stdout = open(output_file, "w")

	client(input_file, output_file)
	# client()

	sys.stdin = sys.__stdin__
	# sys.stdout = sys.__stdout__

	if output_file != sys.__stdout__:
		f1 = open(output_file, "r")
		last_line = f1.readlines()[-1]
		f1.close()
		x = last_line.count(", ") + 1
		print(str(x) + " of " + str(num_of_lines))
		print("ratio: " + str(x / num_of_lines))
		last_line = last_line.split("\'], [\'")
		last_line[0] = last_line[0][3:]
		last_line[len(last_line) - 1] = last_line[len(last_line) - 1][:-4]
		# for line in last_line:
		# 	print(line)


def run_many_clients(num_of_clients=3):
	clients = []
	for i in range(num_of_clients):
		print("start client No. " + str(i) + ":")
		clients.append(Thread(group=None, target=run_client, args=(["input" + str(i), "output" + str(i)])))
	for cli in clients:
		cli.start()
	for cli in clients:
		cli.join()
	print("clients finished")


if __name__ == '__main__':
	# run_many_clients(1)
	# f1 = open("aa1", "w")
	# f2 = open("aa2", "w")
	# f3 = open("aa3", "w")
	# f4 = open("aa4", "w")
	# f1.write("aaa\n")
	# print("hi aaa ", file=f1)
	# print("hi hi ", file=f2)
	# print("hi hi ", file=f3)
	# print("hi hi ", file=f4)
	# sys.stdout.write("bbb")
	# run_client(sys.__stdin__, sys.__stdout__)
	# run_client(sys.__stdin__, "output.txt")
	run_client("input.txt", "output.txt")
	# print(sys.__stdin__.readline())
	# f1 = open("aa1", "r")
	# print(f1.readline())
	# a = "dshg\n"
	# print(a[:-1])
	# print(a)
