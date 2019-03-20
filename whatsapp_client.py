import client
import ssss_lib
import random
import warnings
import threading
from constants import *
import time


class WhatsappClient:
    def __init__(self, servers_list):
        self.__servers_list = servers_list
        self.__clients = []
        self.__msg_str = ""
        self.__keep_running = True
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
                vector_of_msgs.append(int_to_bytes(msg[index][1]))
                assert msg[index][1] == int_from_bytes(int_to_bytes(msg[index][1]))
            cli.run_client_to_server(vector_of_msgs)

    def __create_msg(self):
        print("enter your msg: ")
        self.__msg_str = input()
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
        self.__send_to_servers(vector_of_points)
        if self.__msg_str == "":
            print("you've sent an empty msg to the servers in order to maintain anonymity in the group")
        else:
            print("your msg was sent successfully, you can now send a new msg")
        self.__msg_str = ""

    def __stop_running(self):
        self.__keep_running = False

    def run_client(self):
        # ask the user what he would like to do?
        # a. add new server (should this be automatic?)
        # b. send an honest msg to the servers
        # c. read the msgs that sent
        # d. send empty msg
        # e. exit the program
        while self.__keep_running:
            msg_to_client = "What would you like to do?\n" \
                            "(s)end an honest msg\n" \
                            "(r)ead the msgs that were sent\n" \
                            "(q)uit\n"
            action = input(msg_to_client)
            if action == "s":
                self.__create_msg()
            if action == "r":
                print("not available right now")
            if action == "q":
                self.__stop_running()

    def sending_msgs(self):
        while self.__keep_running:
            if int(time.time()) % EPOCH == 0:
                self.__send_msg()
                time.sleep(1)


if __name__ == "__main__":
    my_client = WhatsappClient([(local_host, i) for i in SERVER_PORTS])
    client_actions_thread = threading.Thread(group=None, target=my_client.run_client, name="client action thread")
    client_sending_msgs_thread = threading.Thread(group=None, target=my_client.sending_msgs,
                                                  name="client sending msgs thread")
    client_sending_msgs_thread.start()
    client_actions_thread.start()

    client_sending_msgs_thread.join()
    client_actions_thread.join()
    my_client.close_connection()
