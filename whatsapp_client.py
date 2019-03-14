import client
import ssss_lib
import random

LEN_OF_BOARD = 10

def int_to_bytes(x):
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')


def int_from_bytes(xbytes):
    return int.from_bytes(xbytes, 'big')


class WhatsappClient:
	def __init__(self, servers_list):
		self.__servers_list = servers_list

	def __send_to_servers(self, vector_of_points):
		for index, server in enumerate(self.__servers_list):
			host, port = server
			vector_of_msgs = []
			for msg in vector_of_points:
				vector_of_msgs.append(int_to_bytes(msg[index][1]))
			client.run_client_to_server(host, port, 1, vector_of_msgs, 0)

	def __create_msg(self):
		num_of_servers = len(self.__servers_list)
		print("enter your msg: ")
		msg_str = input()
		points = ssss_lib.generate_secret_from_msg(msg_str, num_of_servers - 1, num_of_servers)
		vector_of_points = []
		for i in range(LEN_OF_BOARD):
			vector_of_points.append(ssss_lib.generate_secret_from_msg("", num_of_servers - 1, num_of_servers))
		vector_of_points[random.randint(0, LEN_OF_BOARD)] = points
		self.__send_to_servers(vector_of_points)

		print("your msg was sent successfully")


	def __send_noise_to_all_locations_in_board(self):
		num_of_servers = len(self.__servers_list)
		vector_of_points = []
		for i in range(LEN_OF_BOARD):
			vector_of_points.append(ssss_lib.make_fake_msg(num_of_servers))
		self.__send_to_servers(vector_of_points)

		print("board corrupted successfully")

	def __send_nothing(self):
		num_of_servers = len(self.__servers_list)
		vector_of_points = []
		for i in range(LEN_OF_BOARD):
			vector_of_points.append(ssss_lib.generate_secret_from_msg("", num_of_servers - 1, num_of_servers))
		self.__send_to_servers(vector_of_points)

		print("anonymity saved for all of us!")

	def run_client(self):
		# ask the user what he would like to do?
		# a. add new server (should this be automatic?)
		# b. send an honest msg to the servers
		# c. read the msgs that sent
		# d. send gibbrish in order to break the msgs of this epoch
		# e. exit the program
		while True:
			print("What would you like to do?\n"
			      "(s)end a honest msg\n"
			      "(r)ead the msgs that were sent\n"
			      "(a)ttack the server with fake msgs to distroy the board\n"
			      "(q)uit")
			action = input()
			if action == "s":
				self.__create_msg()
			if action == "r":
				print("not available right now")
			if action == "a":
				self.__send_noise_to_all_locations_in_board()
			if action == "q":
				break
# 			TODO - if nothing from client for t time - run __send_nothing

if __name__ == "__main__":
	my_client = WhatsappClient([("127.0.0.1", 9000), ("127.0.0.1", 9001), ("127.0.0.1", 9002), ("127.0.0.1", 9003)])
	my_client.run_client()
