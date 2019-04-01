import time
import server
from constants import *
import random
from multiprocessing import Process
from time import sleep

servers = []


def print_time(a='default'):
	print("From print_time", time.time(), a)


def run_servers():
	evil = random.randint(0, len(SERVER_PORTS) - 1)
	for index, port in enumerate(SERVER_PORTS):
		is_evil = False
		if index == evil:
			is_evil = True
			print("server port " + str(port) + " is evil")
		name = "server thread no. " + str(index) + " is evil == " + str(is_evil)
		servers.append(Process(target=server.start_new_server, name=name, args=(local_host, port, is_evil)))
	for ser in servers:
		ser.start()
	sleep(2)


def kill_servers():
	global servers
	for ser in servers:
		ser.terminate()
	servers = []


if __name__ == "__main__":
	# Example usage
	run_servers()
