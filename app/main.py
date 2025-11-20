import socket  # noqa: F401


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # TODO: Uncomment the code below to pass the first stage
    
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("Server is running on port 4221")

    conn, addr = server_socket.accept() # wait for client
    data = conn.recv(1024).decode()
    print(data)
    if data.startswith("GET / HTTP/1.1"):
        conn.sendall(b"HTTP/1.1 200 OK\r\n\r\nHello, World!") # wait for client
    elif data.startswith("GET /echo/"):
        endpoint = data.split('/')[2][:-5]
        conn.sendall("HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/plain\r\n"
                    "Content-Length: {}\r\n\r\n{}"
                     .format(len(endpoint), endpoint).encode())
    elif data.startswith("GET /user-agent"):
        headers = data.split("\r\n")
        endpoint = ''
        for h in headers:
            if h.startswith("User-Agent:"):
                endpoint = h[len("User-Agent:"):].strip()

        conn.sendall("HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/plain\r\n"
                    "Content-Length: {}\r\n\r\n {}"
                    .format(len(endpoint), endpoint).encode())

    else:
        conn.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n") # wait for client


if __name__ == "__main__":
    main()

