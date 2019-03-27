import client
import ssss_lib
import random
import warnings
import threading
from constants import *
import time
import pickle
import sys


class WhatsappClient:
	""""
	A client that can send a message once an epoch and read all of the previously sent messages from the group.
	At any time the user can save a message (overwriting earlier saved messages) and once an epoch it splits the
	messages into 4 parts and sends them to the four servers.
	"""
	def __init__(self, servers_list, inputf=sys.__stdin__, outputf=sys.__stdout__):
		self.__msg_read_counter = 0
		self.__msg_mutex = threading.Lock()
		self.__servers_list = servers_list
		self.__clients = []
		self.__msg_str = ""
		self.__keep_running = True
		self.__board_history = []
		self.__input = inputf
		self.__output = outputf
		for i in range(len(servers_list)):
			self.__clients.append(client.Client(servers_list[i][0], servers_list[i][1]))

	def close_connection(self):
		for cli in self.__clients:
			cli.close_connection()

	def __get_num_of_servers(self):
		num = len(self.__servers_list)
		if num == 1:
			num = 4
			warnings.warn("For debug purposes only, can't recover messages!!!")
		return num

	def __send_to_servers(self, vector_of_points):
		for index, cli in enumerate(self.__clients):
			vector_of_msgs = []
			for msg in vector_of_points:
				vector_of_msgs.append(msg[index][1])
			to_send = pickle.dumps(vector_of_msgs)
			assert vector_of_msgs == pickle.loads(to_send)
			cli.run_client_to_server(to_send)

	def __create_msg(self):
		print("Enter your message: ")
		temp = self.__input.readline()[:-1]
		self.__msg_mutex.acquire()
		try:
			self.__msg_str = temp
		finally:
			self.__msg_mutex.release()
		print("Your message was saved successfully, you can create a new message but your old message will be overwritten.\n")

	def __send_msg(self):
		num_of_servers = self.__get_num_of_servers()
		num_of_evil_servers = (num_of_servers - 1) // 3
		points = ssss_lib.generate_secret_from_msg(self.__msg_str, num_of_evil_servers + 1, num_of_servers)
		vector_of_points = []
		for i in range(LEN_OF_BOARD):
			vector_of_points.append(
				ssss_lib.generate_secret_from_msg("", num_of_evil_servers + 1, num_of_servers))
		vector_of_points[random.randint(0, LEN_OF_BOARD - 1)] = points
		self.__send_to_servers(vector_of_points)
		if self.__msg_str != "":
			print("your message was sent successfully, you can now prepare a new message.\n")
		# else:
		# 	self.__output.write("You sent an empty message to the servers in order to maintain anonymity in the group.\n")
		self.__msg_mutex.acquire()
		try:
			self.__msg_str = ""
		finally:
			self.__msg_mutex.release()

	def __stop_running(self):
		self.__keep_running = False

	def run_client(self):
		from time import sleep
		while self.__keep_running:
			sleep(EPOCH)
			msg_to_client = "What would you like to do?\n" \
							"(s)end a message\n" \
							"(r)ead unread messages that were sent\n" \
							"(d)ump all messages\n"\
							"(q)uit"
			print(msg_to_client)
			action = self.__input.readline()[:-1]
			if action == "s":
				self.__create_msg()
			if action == "r":
				self.read_last_msgs()
			if action == "d":
				self.read_all_msgs()
			if action == "q":
				sleep(EPOCH)
				self.__stop_running()

	def __get_msgs(self):
		board = []
		for index, cli in enumerate(self.__clients):
			temp = []
			for msg in cli.get_msgs_from_server():
				temp.append((index + 1, msg))
			if len(temp) != 0:
				board.append(temp)
		vector_of_points = list(map(list, zip(*board)))
		msgs = []
		for shares in vector_of_points:
			result = [[shares[i], shares[j]] for i in range(len(shares)) for j in range(i + 1, len(shares))]
			recovered = [ssss_lib.recover_secret(i) for i in result]
			int_msg = max(set(recovered), key=recovered.count)
			if int_msg != 0:
				msgs.append(ssss_lib.int_to_str(int_msg))
		if len(msgs) != 0:
			self.__board_history.append(msgs)

	def talking_with_server(self):
		while self.__keep_running:
			# send the server the message once an EPOCH on the EPOCH
			if int(time.time()) % EPOCH == 0:
				self.__send_msg()
				self.__get_msgs()
				time.sleep(1)

	def read_all_msgs(self):
		print(self.__board_history)
		self.__output.write(str(self.__board_history) + "\n")
		self.__msg_read_counter = len(self.__board_history)

	def read_last_msgs(self):
		if len(self.__board_history) != 0:
			index = self.__msg_read_counter
			self.__msg_read_counter = len(self.__board_history)
			print(self.__board_history[index:])
			self.__output.write(str(self.__board_history[index:]) + "\n")


def main(inputf=sys.__stdin__, outputf=sys.__stdout__):
	if inputf != sys.__stdin__ and inputf != sys.stdin:
		inputf = open(inputf, "r")
	if outputf != sys.__stdout__ and inputf != sys.stdout:
		outputf = open(outputf, "w")
	my_client = WhatsappClient([(local_host, i) for i in SERVER_PORTS], inputf, outputf)
	client_actions_thread = threading.Thread(group=None, target=my_client.run_client, name="client action thread")
	client_sending_msgs_thread = threading.Thread(group=None, target=my_client.talking_with_server,
												  name="client sending msgs thread")
	client_sending_msgs_thread.start()
	client_actions_thread.start()

	client_sending_msgs_thread.join()
	client_actions_thread.join()
	my_client.close_connection()

	if inputf != sys.__stdin__ and inputf != sys.stdin:
		inputf.close()
	if outputf != sys.__stdout__ and inputf != sys.stdout:
		outputf.close()


if __name__ == "__main__":
	main()
