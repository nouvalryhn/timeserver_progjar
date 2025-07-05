
from socket import *
import socket
import threading
import logging
import time
from datetime import datetime

class ProcessTheClient(threading.Thread):
	def __init__(self,connection,address):
		self.connection = connection
		self.address = address
		threading.Thread.__init__(self)

	def run(self):
		logging.warning(f"Connection from {self.address}")
		full_data = ""
		while True:
			try:
				data = self.connection.recv(32).decode('utf-8')
				if data:
					full_data += data
					if "\r\n" in full_data:
						request = full_data.strip()
						logging.warning(f"Received request: {request} from {self.address}")
						if request == "TIME":
							now = datetime.now()
							waktu = now.strftime("%H:%M:%S")
							response = f"JAM {waktu}\r\n"
							self.connection.sendall(response.encode('utf-8'))
							logging.warning(f"Sent response: {response.strip()} to {self.address}")
						elif request == "QUIT":
							logging.warning(f"Client {self.address} sent QUIT. Closing connection.")
							break
						else:
							logging.warning(f"Unknown request: {request} from {self.address}")
						full_data = "" # Reset buffer after processing a full request
				else:
					logging.warning(f"No more data from {self.address}. Closing connection.")
					break
			except Exception as e:
				logging.error(f"Error handling client {self.address}: {e}")
				break
		self.connection.close()
		logging.warning(f"Connection with {self.address} closed.")

class Server(threading.Thread):
	def __init__(self):
		self.the_clients = []
		self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		threading.Thread.__init__(self)

	def run(self):
		self.my_socket.bind(('0.0.0.0',45000)) 
		self.my_socket.listen(1)
		logging.warning("Time Server started on port 45000")
		while True:
			self.connection, self.client_address = self.my_socket.accept()
			logging.warning(f"Connection from {self.client_address}")
			
			clt = ProcessTheClient(self.connection, self.client_address)
			clt.start()
			self.the_clients.append(clt)
	

def main():
	svr = Server()
	svr.start()

if __name__=="__main__":
	main()

