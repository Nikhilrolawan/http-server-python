import socket  # noqa: F401
import threading
import os
import sys


def handle_response(conn, request):

    if request.startswith("GET / HTTP/1.1"):
        conn.sendall(b"HTTP/1.1 200 OK\r\n\r\nHello, World!") # wait for client

    elif request.startswith("GET /echo/"):
        endpoint = request.split('/')[2][:-5]
        conn.sendall("HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/plain\r\n"
                    "Content-Length: {}\r\n\r\n{}"
                    .format(len(endpoint), endpoint).encode())
        
    elif request.startswith("GET /user-agent"):
        headers = request.split("\r\n")
        endpoint = ''
        for h in headers:
            if h.startswith("User-Agent:"):
                endpoint = h[len("User-Agent:"):].strip()

        conn.sendall("HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/plain\r\n"
                    "Content-Length: {}\r\n\r\n{}"
                    .format(len(endpoint), endpoint).encode())
        
    elif request.startswith("GET /files"):
        directory = ""
        if len(sys.argv) > 2 and sys.argv[1] == "--directory":
            directory = sys.argv[2]
        path = os.path.join(directory, request.split()[1][len('/files/'):])
        content = ''
        if os.path.exists(path):
            with open(path, 'r') as f:
                content = f.read()
            conn.sendall("HTTP/1.1 200 OK\r\n"
                        "Content-Type: application/octet-stream\r\n"
                        "Content-Length: {}\r\n\r\n{}"
                        .format(os.path.getsize(path), str(content)).encode())
        else:
            conn.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n") # wait for client

    else:
        conn.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n") # wait for client

def handle_request(conn):
    request = conn.recv(1024).decode()
    handle_response(conn, request)
    conn.close()

def main():
    
    print("Logs of program will appear here!")
    
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("Server is running on port 4221")
    while True:
        server_socket.listen()
        conn, addr = server_socket.accept() 
        threading.Thread(target=handle_request, args=(conn,)).start()


if __name__ == "__main__":
    main()

