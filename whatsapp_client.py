import client
import ssss_lib
import random
import warnings
from constants import *


class WhatsappClient:
    def __init__(self, servers_list):
        self.__servers_list = servers_list
        self.__clients = []
        for i in range(len(servers_list)):
            self.__clients.append(client.Client(servers_list[i][0], servers_list[i][1], 1))

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
                vector_of_msgs.append(int_to_bytes(msg[index][1]))
                assert msg[index][1] == int_from_bytes(int_to_bytes(msg[index][1]))
            cli.run_client_to_server(vector_of_msgs)

    def __create_msg(self):
        num_of_servers = self.__get_num_of_servers()
        num_of_evil_servers = (num_of_servers - 1) // 3
        print("enter your msg: ")
        msg_str = input()
        points = ssss_lib.generate_secret_from_msg(msg_str, num_of_evil_servers + 1, num_of_servers)
        vector_of_points = []
        for i in range(LEN_OF_BOARD):
            vector_of_points.append(
                ssss_lib.generate_secret_from_msg("", num_of_evil_servers + 1, num_of_servers))
        vector_of_points[random.randint(0, LEN_OF_BOARD)] = points
        self.__send_to_servers(vector_of_points)

        print("your msg was sent successfully")

    def __send_nothing(self):
        num_of_servers = self.__get_num_of_servers()
        num_of_evil_servers = (num_of_servers - 1) // 3
        vector_of_points = []
        for i in range(LEN_OF_BOARD):
            vector_of_points.append(
                ssss_lib.generate_secret_from_msg("", num_of_evil_servers + 1, num_of_servers))
        self.__send_to_servers(vector_of_points)

        print("anonymity saved for all of us!")

    def run_client(self):
        # ask the user what he would like to do?
        # a. add new server (should this be automatic?)
        # b. send an honest msg to the servers
        # c. read the msgs that sent
        # d. send empty msg
        # e. exit the program
        while True:
            msg_to_clinet = "What would you like to do?\n" \
                            "(s)end an honest msg\n" \
                            "(r)ead the msgs that were sent\n" \
                            "send an (e)mpty msg\n" \
                            "(q)uit\n"
            action = input(msg_to_clinet)
            if action == "s":
                self.__create_msg()
            if action == "r":
                print("not available right now")
            if action == "e":
                self.__send_nothing()
            if action == "q":
                break


# 			TODO - if nothing from client for t time - run __send_nothing

if __name__ == "__main__":
    my_client = WhatsappClient([("127.0.0.1", 9000)])
    my_client.run_client()
