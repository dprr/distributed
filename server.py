import sys
import socket
import selectors
import types
import pickle
from constants import *
import time

# TODO - the server died when the client exit.
# TODO - create an evil server (can send gibberish)
# TODO - why does client received only her own msgs only? (and not everyone's)

class Server:
	def __init__(self, host, port):
		self.selector = selectors.DefaultSelector()
		self.__message_vector = [0] * LEN_OF_BOARD
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

	def service_connection(self, key, mask):
		sock = key.fileobj
		data = key.data
		if mask & selectors.EVENT_READ:
			recv_data = sock.recv(SIZE_OF_MSG)  # Should be ready to read
			if recv_data:
				data.outb += recv_data
			else:
				print("closing connection to", data.addr)
				self.selector.unregister(sock)
				sock.close()
			received_data = pickle.loads(data.outb)
			self.__message_vector = [a + b for a, b in zip(received_data, self.__message_vector)]
		if mask & selectors.EVENT_WRITE:
			if data.outb:
				sent = sock.send(pickle.dumps(self.__message_vector))
				data.outb = data.outb[sent:]
				assert len(data.outb) == 0
				self.__message_vector = [0] * LEN_OF_BOARD


	def __return_to_client(self):
		while True:
			if int(time.time()) % EPOCH == 0:
				# send_to_clients(self.__message_vector)
				self.__message_vector = [0] * LEN_OF_BOARD
				time.sleep(1)

	def run_server(self):
		try:
			while True:
				keys = self.selector.select(timeout=None)
				for key, mask in keys:
					if key.data is None:
						self.accept_wrapper(key.fileobj)
					else:
						self.service_connection(key, mask)
		except KeyboardInterrupt:
			print("caught keyboard interrupt, exiting")
		finally:
			self.selector.close()


if __name__ == '__main__':
	if len(sys.argv) != 3:
		print("usage:", sys.argv[0], "<host> <port>")
		sys.exit(1)
	host, port = sys.argv[1], int(sys.argv[2])
	s = Server(host, port)
	s.run_server()
