import socket
import threading

class GameClient:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False
    
    def connect(self):
        """Connect to the game server."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.connected = True
            print(f"Connected to server at {self.host}:{self.port}")
            
            # Start receiving messages in a separate thread
            receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
            receive_thread.start()
        except Exception as e:
            print(f"Failed to connect to server: {e}")
            self.connected = False
    
    def send_message(self, message):
        """Send a message to the server."""
        if self.connected:
            try:
                self.socket.sendall(message.encode('utf-8'))
            except Exception as e:
                print(f"Failed to send message: {e}")
                self.connected = False
    
    def receive_messages(self):
        """Receive messages from the server."""
        while self.connected:
            try:
                data = self.socket.recv(1024).decode('utf-8')
                if data:
                    print(f"Server: {data}")
                else:
                    self.connected = False
                    break
            except Exception as e:
                print(f"Error receiving message: {e}")
                self.connected = False
                break
    
    def disconnect(self):
        """Disconnect from the server."""
        if self.socket:
            self.socket.close()
            self.connected = False
            print("Disconnected from server")

if __name__ == "__main__":
    client = GameClient()
    client.connect()
    
    try:
        while client.connected:
            user_input = input("Enter message (or 'quit' to exit): ")
            if user_input.lower() == 'quit':
                break
            client.send_message(user_input)
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        client.disconnect()
