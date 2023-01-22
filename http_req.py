from collections import namedtuple


HttpRequest = namedtuple("HttpRequest", ["method", "path", "headers", "content"])


async def read_request(reader):
    method, path = await read_first_line(reader)
    headers = await read_headers(reader)
    content_length = int(headers.get("Content-Length", 0))
    content = await reader.readexactly(content_length)
    return HttpRequest(
        method=method,
        path=path,
        headers=headers,
        content=content,
    )


async def read_first_line(reader):
    line = await reader.readline()
    if len(line) == 0:
        raise EOFError()
    split = line.strip().decode().split(" ")
    if len(split) != 3:
        raise Exception(f"bad http request first line: {line}")
    method, path, version = split
    if method not in ["GET", "POST"]:
        raise Exception(f"unsupported http request method: {method}")
    if version not in ["HTTP/1.1"]:
        raise Exception(f"unsupported http request version: {version}")
    return method, path


async def read_headers(reader):
    headers = {}
    while True:
        line = await reader.readline()
        line = line.strip().decode()
        if len(line) == 0:
            break
        split = line.split(":", 1)
        if len(split) < 2:
            raise Exception(f"bad http request header: {line}")
        key, val = split
        headers[key.strip()] = val.strip()
    return headers


def parse_path(path):
    if "#" in path:
        path, fragment = path.split("#", 1)
    else:
        fragment = ""
    if "?" in path:
        path, args_str = path.split("?", 1)
        if "&" in args_str:
            args_strs = args_str.split("&")
        else:
            args_strs = [args_str]
        args = {}
        for arg in args_strs:
            if "=" in arg:
                key, val = arg.split("=", 1)
                args[key] = val
            else:
                args[arg] = None            
    else:
        args = {}
    return path, args, fragment
    
        
        
