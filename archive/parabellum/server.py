
import socket
import threading
from durapy.src.unipy.uniCLI import console_print

HOST = str('0.0.0.0')
PORT = int(5000)

clients = []

def _handle_client(connection: socket.socket, address: tuple[str, ...]) -> None:
    """
    Handle a client.
    
    Args
    ----
    
    `connection`: The `socket`.`socket` object of the connection.
    
    `address`: A tupe of the host and port of the server.
    """
    
    console_print("SERVER", "green", f'CONNECTED: {address}')
    
    while True:
        try:
            data = connection.recv(1024).decode()
            if not data:
                break
            console_print(address, "blue", data)
            connection.sendall(f"ACK: {data}".encode())
        except:
            break
        
    console_print("SERVER", "red", f'DISCONNECTED: {address}')
    
    connection.close()
    clients.remove(connection)

def server_kernel() -> None:
    """
    The kernel for the server.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    
    console_print("SERVER", "green", f"Listening on HOST: {HOST}| PORT: {PORT}")
    
    while True:
        connection, address = server.accept()
        clients.append(connection)
        thread = threading.Thread(target=_handle_client, args=(connection, address))
        thread.start()
    
if __name__ == "__main__":
    server_kernel()
