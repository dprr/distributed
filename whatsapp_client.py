import client
import ssss_lib
import random
import warnings
import threading
from constants import *
import time
import pickle


class WhatsappClient:
	def __init__(self, servers_list):
		self.__msg_read_counter = 0
		self.__msg_mutex = threading.Lock()
		self.__servers_list = servers_list
		self.__clients = []
		self.__msg_str = ""
		self.__keep_running = True
		self.__board_history = []
		for i in range(len(servers_list)):
			self.__clients.append(client.Client(servers_list[i][0], servers_list[i][1]))

	def close_connection(self):
		for cli in self.__clients:
			cli.close_connection()

	def __get_num_of_servers(self):
		num = len(self.__servers_list)
		if num == 1:
			num = 4
			warnings.warn("for debug purpose only, can't recover msgs!!!")
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
		temp = input("enter your msg: ")
		self.__msg_mutex.acquire()
		try:
			self.__msg_str = temp
		finally:
			self.__msg_mutex.release()
		print("your msg was saved successfully, you can create new msg but your old msg will be deleted")

	def __send_msg(self):
		num_of_servers = self.__get_num_of_servers()
		num_of_evil_servers = (num_of_servers - 1) // 3
		points = ssss_lib.generate_secret_from_msg(self.__msg_str, num_of_evil_servers + 1, num_of_servers)
		vector_of_points = []
		for i in range(LEN_OF_BOARD):
			vector_of_points.append(
				ssss_lib.generate_secret_from_msg("", num_of_evil_servers + 1, num_of_servers))
		vector_of_points[random.randint(0, LEN_OF_BOARD - 1)] = points
		# vector_of_points[3] = points
		self.__send_to_servers(vector_of_points)
		if self.__msg_str == "":
			print("you've sent an empty msg to the servers in order to maintain anonymity in the group")
		else:
			print("your msg was sent successfully, you can now send a new msg")
		self.__msg_mutex.acquire()
		try:
			self.__msg_str = ""
		finally:
			self.__msg_mutex.release()

	def __stop_running(self):
		self.__keep_running = False

	def run_client(self):
		while self.__keep_running:
			msg_to_client = "What would you like to do?\n" \
							"(s)end an honest msg\n" \
							"(r)ead unread msgs that were sent\n" \
							"(d)ump all msgs\n"\
							"(q)uit\n"
			action = input(msg_to_client)
			if action == "s":
				self.__create_msg()
			if action == "r":
				self.read_last_msgs()
			if action == "d":
				self.read_all_msgs()
			if action == "q":
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
			# DOTO - recover secret with evil server
			result = [[shares[i], shares[j]] for i in range(len(shares)) for j in range(i + 1, len(shares))]
			recovered = [ssss_lib.recover_secret(i) for i in result]
			int_msg = max(set(recovered), key=recovered.count)
			if int_msg != 0:
				msgs.append(ssss_lib.int_to_str(int_msg))
		self.__board_history.append(msgs)

	def talking_with_server(self):
		while self.__keep_running:
			if int(time.time()) % EPOCH == 0:
				self.__send_msg()
				self.__get_msgs()
				time.sleep(1)

	def read_all_msgs(self):
		print(self.__board_history)
		self.__msg_read_counter = len(self.__board_history)

	def read_last_msgs(self):
		if len(self.__board_history) != 0:
			index = self.__msg_read_counter
			self.__msg_read_counter = len(self.__board_history)
			print(self.__board_history[index:])


if __name__ == "__main__":
	my_client = WhatsappClient([(local_host, i) for i in SERVER_PORTS])
	client_actions_thread = threading.Thread(group=None, target=my_client.run_client, name="client action thread")
	client_sending_msgs_thread = threading.Thread(group=None, target=my_client.talking_with_server,
												  name="client sending msgs thread")
	client_sending_msgs_thread.start()
	client_actions_thread.start()

	client_sending_msgs_thread.join()
	client_actions_thread.join()
	my_client.close_connection()
