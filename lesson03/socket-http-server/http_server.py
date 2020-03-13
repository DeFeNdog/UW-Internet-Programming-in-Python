import socket
import sys
import traceback
import mimetypes
import os


def response_ok(body=b"", mimetype=b""):
    """
    returns a basic HTTP response
    """
    return b"\r\n".join([
        b"HTTP/1.1 200 OK",
        b"Content-Type: " + mimetype,
        b"",
        body
    ])


def response_method_not_allowed(body=b"", mimetype=b""):
    """Returns a 405 Method Not Allowed response"""
    return b"\r\n".join([
        b"HTTP/1.1 405 Method Not Allowed",
        b"Content-Type: " + mimetype,
        b"",
        body
    ])


def response_not_found(body=b"", mimetype=b""):
    """Returns a 404 Not Found response"""
    return b"\r\n".join([
        b"HTTP/1.1 404 Not Found",
        b"Content-Type: " + mimetype,
        b"",
        body
    ])


def parse_request(request):
    """
    Given the content of an HTTP request, returns the path of that request.

    This server only handles GET requests, so this method shall raise a
    NotImplementedError if the method of the request is not GET.
    """
    method, path, version = request.split("\r\n")[0].split(" ")
    if method != 'GET':
        raise NotImplementedError

    return path


def response_path(path):
    """
    Returns file or directory contents and mime type
    """
    root_path = os.getcwd()
    content = ""
    mode = "r"
    mime_type = "text/plain"
    request_path = os.path.join(root_path, 'webroot', path.strip("/"))

    if os.path.exists(request_path):

        if os.path.isdir(request_path):
            # directories
            content = '\n'.join(os.listdir(request_path))
            mime_type = ""

        if os.path.isfile(request_path):
            # files
            fname = request_path.split('/')[-1]
            mime_type = mimetypes.guess_type(fname)[0]
            print(mime_type)
            if mime_type == "image/png" or mime_type == "image/jpeg":
                mode = "rb"

            elif mime_type == "text/html":
                mode = "r"

            elif mime_type == "text/plain":
                mode = "r"

            elif mime_type == "text/x-python":
                mode = "r"
            else:
                # not a supported file type
                raise NotImplementedError

            with open(request_path, mode) as file:
                content = file.read()

        if mime_type != "image/png" and mime_type != "image/jpeg":
            # image already encoded
            content = content.encode()

        mime_type = mime_type.encode()

    else:
        raise NameError

    return content, mime_type


def server(log_buffer=sys.stderr):
    address = ('localhost', 10000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("making a server on {0}:{1}".format(*address), file=log_buffer)
    sock.bind(address)
    sock.listen(1)

    try:
        while True:
            print('waiting for a connection', file=log_buffer)
            conn, addr = sock.accept()  # blocking
            try:
                print('connection - {0}:{1}'.format(*addr), file=log_buffer)

                request = ''
                while True:
                    data = conn.recv(1024)
                    request += data.decode('utf8')

                    if '\r\n\r\n' in request:
                        break

                print("Request received:\n{}\n\n".format(request))

                try:
                    path = parse_request(request)
                    content, mimetype = response_path(path)

                    response = response_ok(
                        body=content,
                        mimetype=mimetype
                    )

                except NotImplementedError:
                    response = response_method_not_allowed(
                        body = b"<!DOCTYPE html><html><h1>Not Implemented.</h1></html>",
                        mimetype=b"text/html"
                    )

                except NameError:
                    response = response_not_found(
                        body = b"<!DOCTYPE html><html><h1>Not Found.</h1></html>",
                        mimetype=b"text/html"
                    )

                conn.sendall(response)
            except:
                traceback.print_exc()
            finally:
                conn.close()

    except KeyboardInterrupt:
        sock.close()
        return
    except:
        traceback.print_exc()


if __name__ == '__main__':
    server()
    sys.exit(0)
