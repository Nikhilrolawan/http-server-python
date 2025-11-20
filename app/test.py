# s = "GET /echo/abcef HTTP/1.1\r\nHost: localhost:4221\r\nUser-Agent: curl/7.64.1\r\nAccept: */*\r\n\r\n"
# print(s.split('/')[2][:-5])
s = "GET /user-agent HTTP/1.1\r\n// Headers Host: localhost:4221\r\nUser-Agent: foobar/1.2.3\r\n // Read this value Accept: */*\r\n\r\n"
print(s.split('\r\n'))
headers = s.split("\r\n")
for h in headers:
    if h.startswith("User-Agent:"):
        value = h[len("User-Agent:"):].strip()
        print(value)
