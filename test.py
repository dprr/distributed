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
	print("d", file=f)
	print("q", file=f)
	f.close()


def calc_ratio(input_file, output_file, ratio_file):
	inpt = get_input_lines(input_file)
	outpt, collisions = get_output_lines(output_file)
	if len(inpt) == 0:
		return 0

	own_output = []
	for line in outpt:
		if line in inpt:
			own_output.append(line)

	ratio_set = [len(inpt), len(own_output), collisions]
	ratio_file = open(ratio_file, "w")
	ratio_file.write(str(ratio_set) + "\n")
	return ratio_set


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
	collisions = dump.count('Not ciphertext of utf-8')
	dump = dump[:-1]
	dump = dump.replace(' ', '')
	dump = dump.replace('[', '')
	dump = dump.replace(']', '')
	dump = dump.replace('\'', '')
	dump = dump.split(",")
	return dump, collisions


def get_ratios(ratio_file):
	f1 = open(ratio_file, "r")
	inpt = f1.readline()
	f1.close()
	tmp = inpt[:-1]
	tmp = tmp.replace('[', '')
	tmp = tmp.replace(']', '')
	tmp = tmp.split(", ")
	inpt = int(tmp[0])
	own_output = int(tmp[1])
	collisions = int(tmp[2])
	return inpt, own_output, collisions


def get_misses(ratio_file):
	inpt, own_output, collisions = get_ratios(ratio_file)
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


def collect_data(start_thread=True):
	if start_thread:
		servers_thread = Thread(target=run_servers)
		servers_thread.start()
		sleep(10)
	global LEN_OF_BOARD
	global EPOCH
	board_lengths = list(range(5, 50, 1)) + list(range(50, 100, 2)) + list(range(100, 1000, 50))
	users_num = list(range(2, 100, 1)) + list(range(100, 150, 10)) + list(range(150, 256, 50))
	# board_lengths = [50, 100]
	y = []
	for i in board_lengths:
		LEN_OF_BOARD = i
		for j in users_num:
			if j > i:
				break
			if j < 30:
				EPOCH = 2
			elif j < 60:
				EPOCH = 4
			elif j < 80:
				EPOCH = 6
			elif j < 100:
				EPOCH = 8
			outpt = tuple(run_many_clients(num_of_clients=j, num_of_lines=5, start_thread=False)) + tuple([i])
			y.append(outpt)
	if start_thread:
		sys.exit()
	return y


def run_many_clients(num_of_clients=3, num_of_lines=10, ratio_file="ratios.txt", start_thread=True):
	if start_thread:
		servers_thread = Thread(target=run_servers)
		servers_thread.start()
		sleep(10)
	clients = []
	for i in range(num_of_clients):
		print("start client No. " + str(i) + ":")
		clients.append(Thread(target=run_client,
							  args=(["input" + str(i), "output" + str(i), "ratio" + str(i), num_of_lines, False])))
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
	sum_ratios = (sum_ratios[0] / sum_ratios[1], sum_ratios[0], sum_ratios[1], ratios[0][3], num_of_clients, LEN_OF_BOARD)
	print(ratios)
	print(sum_ratios)
	ratiosf = open(ratio_file, "a")
	ratiosf.write(str(sum_ratios) + "\n")
	ratiosf.close()
	print("clients finished")
	if start_thread:
		sys.exit()
	return sum_ratios


def plot_clients_graph():
	x = range(2, 256)
	y = [run_many_clients(i, start_thread=False)[0] for i in x]
	plt.plot(x, y)
	plt.xlabel('Number of clients')
	plt.ylabel('Percentage of collisions')
	plt.show()


def plot_len_of_board_graph(clients=10):
	global LEN_OF_BOARD
	x = list(range(5, 50, 1)) + list(range(50, 100, 2)) + list(range(100, 1000, 50))
	y = []
	for i in x:
		LEN_OF_BOARD = i
		y.append(run_many_clients(clients, start_thread=False)[0])
	LEN_OF_BOARD = 50
	plt.plot(x, y)
	plt.xlabel('LEN_OF_BOARD')
	plt.ylabel('Percentage of collisions')
	plt.show()


if __name__ == '__main__':
	# print(run_many_clients(15, 10))
	# run_client(num_of_lines=15)
	results = str(collect_data(start_thread=False))
	print(results)
	f1 = open("results.txt", "a")
	f1.write("\n\n" + results)
	f1.close()
