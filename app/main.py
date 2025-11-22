import socket  # noqa: F401
import threading
import os


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
        path = request.split()[1]
        content = ''
        if os.path.exists(path):
            with open(path, 'r') as f:
                content = f.read()
            conn.sendall("HTTP/1.1 200 OK\r\n"
                        "Content-Type: application/octet-stream\r\n"
                        "Content-Length: {}\r\n\r\n{}"
                        .format(os.path.getsize(path), content).encode())
        else:
            conn.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n") # wait for client

    else:
        conn.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n") # wait for client

def handle_request(conn):
    request = conn.recv(1024).decode()
    handle_response(conn, request)
    conn.close()

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # TODO: Uncomment the code below to pass the first stage
    
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("Server is running on port 4221")
    while True:
        server_socket.listen()
        conn, addr = server_socket.accept() # wait for client
        threading.Thread(target=handle_request, args=(conn,)).start()


if __name__ == "__main__":
    main()

