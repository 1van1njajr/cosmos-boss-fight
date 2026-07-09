import socket
import threading
import signal
import sys


class ClassicServer:
	def __init__(self, host='0.0.0.0', port=5000, backlog=5):
		self.host = host
		self.port = port
		self.backlog = backlog
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.clients = []
		self.running = False

	def start(self):
		self.sock.bind((self.host, self.port))
		self.sock.listen(self.backlog)
		self.running = True
		print(f'Server listening on {self.host}:{self.port}')
		try:
			while self.running:
				client_sock, addr = self.sock.accept()
				print(f'Accepted connection from {addr}')
				t = threading.Thread(target=self.handle_client, args=(client_sock, addr), daemon=True)
				t.start()
				self.clients.append((client_sock, addr))
		except OSError:
			pass

	def stop(self):
		self.running = False
		try:
			self.sock.close()
		except Exception:
			pass
		for c, _ in self.clients:
			try:
				c.close()
			except Exception:
				pass
		print('Server stopped')

	def handle_client(self, client_sock: socket.socket, addr):
		with client_sock:
			client_sock.sendall(b'Welcome to ClassicServer\n')
			try:
				while True:
					data = client_sock.recv(1024)
					if not data:
						break
					# Echo back
					client_sock.sendall(b'ECHO: ' + data)
			except ConnectionResetError:
				pass
		print(f'Connection closed: {addr}')


def main():
	server = ClassicServer(port=5000)

	def sigint_handler(signum, frame):
		server.stop()
		sys.exit(0)

	signal.signal(signal.SIGINT, sigint_handler)
	server.start()


if __name__ == '__main__':
	main()

