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


def calc_ratio(init_num_of_lines, output_file):
	# get last dump
	f1 = open(output_file, "r")
	dump = f1.readlines()[-1]
	f1.close()

	# parse dump
	dump = dump.split("\'], [\'")
	dump[0] = dump[0][3:]
	dump[len(dump) - 1] = dump[len(dump) - 1][:-4]

	# calc ratio
	ratio = len(dump) / init_num_of_lines
	print(str(len(dump)) + " of " + str(init_num_of_lines))
	print("ratio: " + str(ratio))
	# for line in dump:
	# 	print(line)
	return ratio


def get_input_lines(input_file):
	f1 = open(input_file, "r")
	inpt = f1.readlines()
	f1.close()
	messages = []
	for i in range(len(inpt)):
		if inpt[i][:-1] == "s":
			messages.append(inpt[i+1][:-1])
			i += 2
	return messages


def run_client(input_file="input.txt", output_file="output.txt", num_of_lines=5):
	# if sys.stdin.isatty():
	# 	exit()

	# generate input
	if input_file != sys.__stdin__:
		gen_input(input_file, num_of_lines)

	client(input_file, output_file)
	# client()

	if output_file != sys.__stdout__ and input_file != sys.__stdin__:
		calc_ratio(num_of_lines, output_file)


def run_many_clients(num_of_clients=3, num_of_lines=5):
	clients = []
	for i in range(num_of_clients):
		print("start client No. " + str(i) + ":")
		clients.append(Thread(group=None, target=run_client, args=(["input" + str(i), "output" + str(i), num_of_lines])))
	for cli in clients:
		cli.start()
	for cli in clients:
		cli.join()
	print("clients finished")


if __name__ == '__main__':
	run_many_clients(4)
	# run_client(sys.__stdin__, sys.__stdout__)
	# run_client(sys.__stdin__, "output.txt")
	# run_client("input.txt", "output.txt")
	# get_input_lines("input.txt")
