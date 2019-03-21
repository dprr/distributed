import sched, time
import server
from constants import *
import random
import threading
s = sched.scheduler(time.time, time.sleep)
def print_time(a='default'):
	print("From print_time", time.time(), a)

def print_some_times():
	print(time.time())
	s.enter(10, 1, print_time)
	print("hi")
	s.enter(5, 2, print_time, argument=('positional',))
	print("hi")
	s.enter(5, 1, print_time, kwargs={'a': 'keyword'})
	print("hi")
	s.run()
	print("hi")
	print(time.time())


def run_servers():
	servers = []
	evil = random.randint(0, len(SERVER_PORTS) - 1)
	for index, port in enumerate(SERVER_PORTS):
		is_evil = False
		if index == evil:
			is_evil = True
			print("server port " + str(port) + " is evil")
		name = "server thread no. " + str(index) + " is evil == " + str(is_evil)
		servers.append(threading.Thread(group=None, target=server.start_new_server, name=name, args=(local_host, port, is_evil)))
	for ser in servers:
		ser.start()
	for ser in servers:
		ser.join()

if __name__ == "__main__":
	# print_some_times()
	run_servers()