from whatsapp_client import main as client
from threading import Thread
import matplotlib.pyplot as plt
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


def calc_ratio(input_file, output_file):
	inpt = get_input_lines(input_file)
	outpt = get_output_lines(output_file)

	print(inpt)
	print(outpt)
	own_output = []
	for line in outpt:
		if line in inpt:
			own_output.append(line)
	print(outpt)

	# calc ratio
	ratio = len(outpt) / len(inpt)
	print(str(len(outpt)) + " of " + str(len(inpt)))
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


def get_output_lines(output_file):
	# get last dump
	f1 = open(output_file, "r")
	dump = f1.readlines()[-1]
	f1.close()

	# parse dump
	dump = dump[:-1]
	dump = dump.replace(' ', '')
	dump = dump.replace('[', '')
	dump = dump.replace(']', '')
	dump = dump.replace('\'', '')
	dump = dump.split(",")
	return dump


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

def plot_clients_graph():
	x = range(1,1000)
	# TODO: change to number of collisions
	y = [run_many_clients(i) for i in x]
	plt.plot(x,y)
	plt.xlabel('Number of clients')
	plt.ylabel('Number of collisions')
	plt.show()

def plot_len_of_board_graph():
	x = range(1,1000)
	# TODO: change to number of collisions
	y = [i for i in x]
	plt.plot(x,y)
	plt.xlabel('LEN_OF_BOARD')
	plt.ylabel('Number of collisions')
	plt.show()

if __name__ == '__main__':
	run_many_clients(4, 10)
	# run_client(sys.__stdin__, sys.__stdout__)
	# run_client(sys.__stdin__, "output.txt")
	# run_client("input.txt", "output.txt")
	# get_input_lines("input.txt")
	# calc_ratio("input0", "output0")
