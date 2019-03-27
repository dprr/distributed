from main import run_servers
from whatsapp_client import main as client
from threading import Thread, Event
import matplotlib.pyplot as plt
import sys
import random
import string
from os import remove
from time import sleep
from constants import *
from os.path import isfile


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


def calc_ratio(input_file, output_file, ratio_file):
	inpt = get_input_lines(input_file)
	outpt = get_output_lines(output_file)
	if len(inpt) == 0:
		return 0

	# print("input: "  + str(inpt))
	# print("output: " + str(outpt))
	own_output = []
	for line in outpt:
		if line in inpt:
			own_output.append(line)
	# print(own_output)

	# calc ratio
	ratio = len(own_output) / len(inpt)
	print(str(len(own_output)) + " out of " + str(len(inpt)))
	print("ratio: " + str(ratio))

	ratio_file = open(ratio_file, "w")
	ratio_file.write(str([ratio, len(own_output), len(inpt)]) + "\n")
	return ratio, len(own_output), len(inpt)


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


def get_ratios(ratio_file):
	f1 = open(ratio_file, "r")
	inpt = f1.readline()
	f1.close()
	tmp = inpt[:-1]
	tmp = tmp.replace('[', '')
	tmp = tmp.replace(']', '')
	tmp = tmp.split(", ")
	ratio = float(tmp[0])
	own_output = int(tmp[1])
	inpt = int(tmp[2])
	return ratio, own_output, inpt


def get_misses(ratio_file):
	ratio, own_output, inpt = get_ratios(ratio_file)
	return inpt - own_output


def run_client(input_file="input.txt", output_file="output.txt", ratio_file="ratio.txt", num_of_lines=5, start_tread=True):
	if start_tread:
		servers_thread = Thread(group=None, target=run_servers, name="servers thread")
		servers_thread.start()
		sleep(10)

	# if sys.stdin.isatty():
	# 	exit()

	# generate input
	if input_file != sys.__stdin__:
		gen_input(input_file, num_of_lines)

	# run client
	client(input_file, output_file)

	if output_file != sys.__stdout__ and input_file != sys.__stdin__:
		calc_ratio(input_file, output_file, ratio_file)
		remove(input_file)
		remove(output_file)

	if start_tread:
		sys.exit()


def run_many_clients(num_of_clients=3, num_of_lines=5, ratio_file="ratio.txt", start_tread=True):
	if start_tread:
		servers_thread = Thread(group=None, target=run_servers, name="servers thread")
		servers_thread.start()
		sleep(10)
	clients = []
	for i in range(num_of_clients):
		print("start client No. " + str(i) + ":")
		clients.append(Thread(group=None, target=run_client, args=(["input" + str(i), "output" + str(i), "ratio" + str(i), num_of_lines, False])))
	for cli in clients:
		cli.start()
	for cli in clients:
		cli.join()

	ratios = []
	sum_ratios = [0, 0]
	for i in range(num_of_clients):
		temp = get_ratios("ratio" + str(i))
		remove("ratio" + str(i))
		ratios.append(temp)
		sum_ratios = (sum_ratios[0] + temp[1], sum_ratios[1] + temp[2])
	sum_ratios = (sum_ratios[0] / sum_ratios[1], sum_ratios[0], sum_ratios[1])
	print(ratios)
	print(sum_ratios)
	ratiosf = open(ratio_file, "w")
	ratiosf.write(str(sum_ratios))
	ratiosf.close()
	print("clients finished")
	if start_tread:
		sys.exit()
	return sum_ratios[2] - sum_ratios[1]


def plot_clients_graph():
	x = range(1, 1000)
	y = [run_many_clients(i) for i in x]
	plt.plot(x,y)
	plt.xlabel('Number of clients')
	plt.ylabel('Number of collisions')
	plt.show()

def plot_len_of_board_graph():
	global LEN_OF_BOARD
	x = list(range(5, 50 ,1)) + list(range(50,100,2)) + list(range(100,1000,50))
	y = []
	for i in x:
		LEN_OF_BOARD = i
		y.append(run_many_clients(i))
	LEN_OF_BOARD = 50
	plt.plot(x,y)
	plt.xlabel('LEN_OF_BOARD')
	plt.ylabel('Number of collisions')
	plt.show()


if __name__ == '__main__':
	# print(run_many_clients(5, 10))
	# run_client(sys.__stdin__, sys.__stdout__, 5)
	# run_client(sys.__stdin__, "output.txt", 5)
	run_client(num_of_lines=15)
	# get_input_lines("input.txt")
	# calc_ratio("input0", "output0")
	# print(get_ratios("ratio_file"))
