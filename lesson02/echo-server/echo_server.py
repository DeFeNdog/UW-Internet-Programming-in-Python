import socket
import sys
import traceback


def server(log_buffer=sys.stderr):

    address = ('127.0.0.1', 10000)

    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_TCP)

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(1)

    print("making a server on {0}:{1}".format(*address), file=log_buffer)

    try:

        while True:

            print('waiting for a connection', file=log_buffer)
            conn, addr = sock.accept()
            buffer_size = 16

            try:
                print('connection - {0}:{1}'.format(*addr), file=log_buffer)

                while True:
                    data = conn.recv(buffer_size)
                    print('received "{0}"'.format(data.decode('utf8')))

                    conn.sendall(data)
                    print('sent "{0}"'.format(data.decode('utf8')))

                    if len(data) < buffer_size:
                        break

            except Exception as e:
                traceback.print_exc()
                sys.exit(1)
                print(
                    'echo complete, client connection closed', file=log_buffer
                )

    except KeyboardInterrupt:
        sock.shutdown(1)
        sock.close()
        return False
        print('quitting echo server', file=log_buffer)


if __name__ == '__main__':
    server()
    sys.exit(0)
