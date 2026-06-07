
import socket
import threading
from durapy import uniCLI

HOST = str('0.0.0.0')
PORT = int(5000)

clients = []

def _handle_client(connection: socket.socket, address: tuple[str, ...]) -> None:
    """
    Handle a client.
    
    Args
    ----
    `connection`: The `socket`.`socket` object of the connection. \n
    `address`: A tupe of the host and port of the server. \n
    """
    
    uniCLI.console_print("SERVER", "green", f'CONNECTED: {address}')
    
    while True:
        try:
            data = connection.recv(1024).decode()
            if not data:
                break
            uniCLI.console_print(address, "blue", data)
            connection.sendall(f"ACK: {data}".encode())
        except:
            break
        
    uniCLI.console_print("SERVER", "red", f'DISCONNECTED: {address}')
    
    connection.close()
    clients.remove(connection)

def server_kernel() -> None:
    """
    The kernel for the server.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    
    uniCLI.console_print("SERVER", "green", f"Listening on HOST: {HOST}| PORT: {PORT}")
    
    while True:
        connection, address = server.accept()
        clients.append(connection)
        thread = threading.Thread(target=_handle_client, args=(connection, address))
        thread.start()
    
if __name__ == "__main__":
    server_kernel()
