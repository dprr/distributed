import sys
import socket
import selectors
import types
from constants import *
from threading import Lock


class Client:
    def __init__(self, host, port):
        self.__received_data_mutex = Lock()
        self.sel = selectors.DefaultSelector()
        server_addr = (host, int(port))
        print("starting connection to", server_addr)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setblocking(False)
        self.sock.connect_ex(server_addr)
        self.events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.data = types.SimpleNamespace(
            recv_total=0,
            messages="",
            outb=b"",
        )
        self.sel.register(self.sock, self.events, data=self.data)
        self.__received_data = ""

    def get_msgs_from_server(self):
        if self.__received_data == "":
            return ""
        else:
            import pickle
            temp = pickle.loads(self.__received_data)
            self.__received_data_mutex.acquire()
            self.__received_data = ""
            self.__received_data_mutex.release()
            return temp

    def service_connection(self, key, mask):
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(SIZE_OF_MSG)  # Should be ready to read
            if recv_data:
                # print("received", repr(recv_data))
                self.__received_data_mutex.acquire()
                self.__received_data = recv_data
                self.__received_data_mutex.release()
                data.recv_total += len(recv_data)
        if mask & selectors.EVENT_WRITE:
            if not data.outb and data.messages:
                data.outb = data.messages
            if data.outb:
                # print("sending", repr(data.outb))
                # print(data.outb)
                sent = sock.send(data.outb)  # Should be ready to write
                data.outb = data.outb[sent:]

    def close_connection(self):
        print("closing connection")
        self.sel.unregister(self.sock)
        self.sock.close()

    def run_client_to_server(self, msg):
        self.data.messages = msg
        try:
            # while True:
            events = self.sel.select(timeout=1)
            if events:
                for key, mask in events:
                    self.service_connection(key, mask)
                # Check for a socket being monitored to continue.
                # if not self.sel.get_map():
                #     break
        except KeyboardInterrupt:
            print("caught keyboard interrupt, exiting")
        # finally:
        #     self.sel.close()
