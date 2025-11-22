import socket  # noqa: F401
import threading
import os
import sys

def send_response(conn, contentSize, content, contentType = "text/plain"):
    return conn.sendall("HTTP/1.1 200 OK\r\n"
                    "Content-Type: {}\r\n"
                    "Content-Length: {}\r\n\r\n{}"
                    .format(contentType, contentSize, content).encode())

def handle_response(conn, request):

    if request.startswith("GET / HTTP/1.1"):
        conn.sendall(b"HTTP/1.1 200 OK\r\n\r\nHello, World!") # wait for client

    elif request.startswith("GET /echo/"):
        endpoint = request.split('/')[2][:-5]
        send_response(conn = conn, contentSize = len(endpoint), content = endpoint)
        
    elif request.startswith("GET /user-agent"):
        headers = request.split("\r\n")
        endpoint = ''
        for h in headers:
            if h.startswith("User-Agent:"):
                endpoint = h[len("User-Agent:"):].strip()
        send_response(conn = conn, contentSize = len(endpoint), content = endpoint)
        
    elif request.startswith("GET /files"):
        directory = ""
        if len(sys.argv) > 2 and sys.argv[1] == "--directory":
            directory = sys.argv[2]
        path = os.path.join(directory, request.split()[1][len('/files/'):])
        content = ""
        if os.path.exists(path):
            with open(path, 'r') as f:
                content = f.read()
            send_response(conn = conn, contentType = "application/octet-stream", contentSize = os.path.getsize(path), content = str(content))
        else:
            conn.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n") # wait for client

    elif request.startswith("POST /files"):
        directory = ""
        if len(sys.argv) > 2 and sys.argv[1] == "--directory":
            directory = sys.argv[2]
        path = os.path.join(directory, request.split()[1][len('/files/'):])
        content = request.split()[-1]
        try:
            with open(path, 'w') as fw:
                fw.write(content)
            conn.sendall(b"HTTP/1.1 201 Created\r\n\r\n") # wait for client
        except:
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

