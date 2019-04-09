from test_servers import *
from whatsapp_client import main as client
from threading import Thread
import matplotlib.pyplot as plt
import sys
import random
import string
from os import remove
from time import sleep
from constants import *
import server
import numpy as np

servers = []
TITLES = ["Percentage of Successfully delivered",
		  "Percentage of Collided messages",
		  "Percentage of Lost messages"]


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
			messages.append(inpt[i + 1][:-1])
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


def parse_line(line):
	import re
	line = re.sub('[\[\]()\'\n]', '', line)
	line = line.split(", ")
	output = []
	for arg in line:
		output.append(int(arg))
	return output


def get_ratio(ratio_file):
	f1 = open(ratio_file, "r")
	inpt_line = parse_line(f1.readline())
	f1.close()
	inpt = int(inpt_line[0])
	own_output = int(inpt_line[1])
	collisions = int(inpt_line[2])
	return inpt, own_output, collisions


def get_misses(ratio_file):
	inpt, own_output, collisions = get_ratio(ratio_file)
	return inpt - own_output


def get_data(ratios_file):
	data = []
	f1 = open(ratios_file, "r")
	for line in f1:
		data.append(parse_line(line))
	f1.close()
	dictionary = {}
	for datum in data:
		if datum[4] not in dictionary:
			dictionary[datum[4]] = {}
		success = datum[1] / datum[0]
		fail = datum[2] / datum[0]
		lost = (datum[0] - datum[1] - datum[2] * 2) / datum[0]
		dictionary[datum[4]][datum[3]] = [success, fail, lost]
	board_sizes = list(dictionary.keys())
	clients = list(dictionary[board_sizes[0]].keys())
	success = np.zeros(shape=[len(board_sizes), len(clients)])
	fail = np.zeros(shape=[len(board_sizes), len(clients)])
	lost = np.zeros(shape=[len(board_sizes), len(clients)])
	for i in range(len(board_sizes)):
		for j in range(len(clients)):
			success[i, j] = dictionary[board_sizes[i]][clients[j]][0]
			fail[i, j] = dictionary[board_sizes[i]][clients[j]][1]
			lost[i, j] = dictionary[board_sizes[i]][clients[j]][2]
	return [success, fail, lost], [board_sizes, clients]


def run_client(input_file="input.txt", output_file="output.txt", ratio_file="ratio.txt", num_of_lines=5,
			   start_servers=True):
	if start_servers:
		run_servers()

	# generate input
	if input_file != sys.__stdin__:
		gen_input(input_file, num_of_lines)

	# run client
	client(input_file, output_file)

	if start_servers:
		kill_servers()
	if output_file != sys.__stdout__ and input_file != sys.__stdin__:
		calc_ratio(input_file, output_file, ratio_file)
		remove(input_file)
		remove(output_file)


def collect_data(start_servers=True, num_of_lines=15, ratio_file="ratios.txt"):
	# if start_servers:
	# 	run_servers()
	ratiosf = open(ratio_file, "a")
	ratiosf.write("\n")
	ratiosf.close()
	global LEN_OF_BOARD
	global EPOCH
	# board_lengths = list(range(5, 50, 1)) + list(range(50, 100, 2)) + list(range(100, 1000, 50))
	board_lengths = list([50, 100])
	# users_num = list(range(2, 100, 1)) + list(range(100, 150, 10)) + list(range(150, 256, 50))
	users_num = list([2, 3])
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
			outpt = tuple(run_many_clients(j, num_of_lines, ratio_file, start_servers))
			y.append(outpt)
	# if start_servers:
	# 	kill_servers()
	return y


def run_many_clients(num_of_clients=3, num_of_lines=10, ratio_file="ratios.txt", start_servers=True):
	if start_servers:
		run_servers()
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
		temp = get_ratio("ratio" + str(i))
		remove("ratio" + str(i))
		ratios.append(temp)
		sum_ratios = (sum_ratios[0] + temp[0], sum_ratios[1] + temp[1])
	sum_ratios = (sum_ratios[0], sum_ratios[1], ratios[0][2], num_of_clients, LEN_OF_BOARD)
	print(ratios)
	print(sum_ratios)
	ratiosf = open(ratio_file, "a")
	ratiosf.write(str(sum_ratios) + "\n")
	ratiosf.close()
	print("clients finished")
	if start_servers:
		kill_servers()
	return sum_ratios


def plot_data(data_file="data.txt", to_save=False):
	data, info = get_data(data_file)
	# a = np.array([[0, 1], [0.2, 0.8]])
	# b = np.array([[0.8, 0.1], [0.2, 0.8]])
	# c = np.array([[0.5, 0.7], [0.2, 0.6]])
	# data = a, b, c
	# info = np.array([[0, 1], [0.2, 0.8]])
	plt.rcParams.update({'font.size': 22})
	fig, ax = plt.subplots(3, sharex='all', sharey='all', figsize=(13, 10))
	plt.xlabel('Number of clients')
	ax[1].set_ylabel('Length of board')
	plt.xticks(np.arange(len(info[1])), info[1])
	plt.yticks(np.arange(len(info[0])), info[0])
	for i in range(3):
		b = ax[i].pcolor(data[i], vmin=0, vmax=1, cmap='jet')
		ax[i].set_title(TITLES[i])
		bounds = list(ax[i].get_position().bounds)
		bounds[2] = 0.7
		ax[i].set_position(pos=bounds)
	cbar_ax = fig.add_axes([0.85, 0.11, 0.05, 0.77])
	fig.colorbar(b, cax=cbar_ax)
	# fig.subplots_adjust(wspace=5000)
	# plt.tight_layout()
	if to_save:
		plt.savefig('data plot.png')
	else:
		plt.show()


if __name__ == '__main__':
	# plot_data(to_save=False)
	plot_data(to_save=True)
	# for i in range(2, 51):
	#	print(run_many_clients(start_servers=True, num_of_lines=100, num_of_clients=i))
	# print(run_many_clients(start_servers=True, num_of_lines=100, num_of_clients=19))
	# run_client(num_of_lines=100, start_servers=True)
	# results = str(collect_data())
	# print(results)
	# for a in data:
	# 	print(data[a])
