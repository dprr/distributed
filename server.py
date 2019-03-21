import sys
import socket
import selectors
import types
import pickle
from constants import *
import random
import time
from threading import Lock

# TODO - why does client received only her own msgs only? (and not everyone's)
PORT = ""
EVIL = False


class Server:
	def __init__(self, host, port):
		self.selector = selectors.DefaultSelector()
		self.__message_vector = [0] * LEN_OF_BOARD
		self.__clients = set()
		self.__clients_mutex = Lock()
		lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		lsock.bind((host, port))
		lsock.listen()
		print("listening on", (host, port))
		lsock.setblocking(False)
		self.selector.register(lsock, selectors.EVENT_READ, data=None)

	def accept_wrapper(self, sock):
		conn, addr = sock.accept()  # Should be ready to read
		print("accepted connection from", addr)
		conn.setblocking(False)
		data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
		events = selectors.EVENT_READ | selectors.EVENT_WRITE
		self.selector.register(conn, events, data=data)
		with self.__clients_mutex:
			self.__clients.add(conn)

	def service_connection(self, key, mask):
		sock = key.fileobj
		data = key.data
		if mask & selectors.EVENT_READ:
			recv_data = b''
			try:
				recv_data = sock.recv(SIZE_OF_MSG)  # Should be ready to read
			except ConnectionResetError:
				exit(0)
			if recv_data:
				data.outb = recv_data
				received_data = pickle.loads(data.outb)
				self.__message_vector = [a + b for a, b in zip(received_data, self.__message_vector)]
			else:
				print("closing connection to", data.addr)
				with self.__clients_mutex:
					self.__clients.remove(sock)
					self.selector.unregister(sock)
					sock.close()

	def reply_to_client(self):
		with self.__clients_mutex:
			for sock in self.__clients:
				if EVIL:
					self.__message_vector = [random.randint(0, PRIME) for _ in range(LEN_OF_BOARD)]
					if random.randint(0, 9) != 0:
						sock.sendall(pickle.dumps(self.__message_vector))
				else:
					sock.sendall(pickle.dumps(self.__message_vector))
			self.__message_vector = [0] * LEN_OF_BOARD

	def run_server(self):
		try:
			while True:
				keys = self.selector.select(timeout=None)
				for key, mask in keys:
					if key.data is None:
						self.accept_wrapper(key.fileobj)
					else:
						self.service_connection(key, mask)
					if int(time.time()) % EPOCH == 5:
						self.reply_to_client()
						time.sleep(1)
		except KeyboardInterrupt:
			print("caught keyboard interrupt, exiting")
		finally:
			self.selector.close()


if __name__ == '__main__':
	if len(sys.argv) < 3:
		print("usage:", sys.argv[0], "<host> <port>")
		sys.exit(1)
	if len(sys.argv) == 4 and sys.argv[3] == "evil":
		EVIL = True
	host, port = sys.argv[1], int(sys.argv[2])
	PORT = port
	s = Server(host, port)
	s.run_server()
