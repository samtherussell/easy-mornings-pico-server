from collections import namedtuple


HttpResponse = namedtuple("HttpResponse", ["status", "headers", "content"])


def send_response(response, writer):
    send_first_line(response.status, writer)
    headers_copy = dict(response.headers)
    headers_copy["Content-Length"] = len(response.content)
    send_headers(headers_copy, writer)
    if len(response.content) > 0:
        writer.write(response.content)
    writer.drain()


status_text_lookup = {
    200: "OK",
    404: "Not Found",
    500: "Internal Server Error",
    501: "Not Implemented",
}

status_lookup = {}
for code, text in status_text_lookup.items():
    status_lookup[text] = code    


def send_first_line(status, writer):
    if type(status) == str:
        status_text = status
        status = status_lookup[status_text]
    else:
        status_text = status_text_lookup[status]
    
    line = f"HTTP/1.1 {status} {status_text}\r\n".encode()
    writer.write(line)


def send_headers(headers, writer):
    for key, value in headers.items():
        line = f"{key}: {value}\r\n".encode()
        writer.write(line)
    writer.write(b"\r\n")    
