# s = "GET /echo/abcef HTTP/1.1\r\nHost: localhost:4221\r\nUser-Agent: curl/7.64.1\r\nAccept: */*\r\n\r\n"
# print(s.split('/')[2][:-5])
# s = "GET /user-agent HTTP/1.1\r\n// Headers Host: localhost:4221\r\nUser-Agent: foobar/1.2.3\r\n // Read this value Accept: */*\r\n\r\n"
# print(s.split('\r\n'))
# headers = s.split("\r\n")
# for h in headers:
#     if h.startswith("User-Agent:"):
#         value = h[len("User-Agent:"):].strip()
#         print(value)
# s = "GET /files/foo.txt HTTP/1.1\r\nHost: localhost:4221\r\nUser-Agent: curl/8.2.1\r\nAccept: */*\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\n\r\n"
# print(s.split()[1][len('/files/'):])
# import sys
# print(sys.argv[0])
s =  "POST /files/number HTTP/1.1\r\nHost: localhost:4221\r\nUser-Agent: curl/7.64.1\r\nAccept: */*\r\nContent-Type: application/octet-stream\r\nContent-Length: 5\r\n\r\n12345"
print(type(s.split()[-1]))