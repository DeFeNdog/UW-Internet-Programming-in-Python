import socket
import sys
import traceback


def client(msg, log_buffer=sys.stderr):
    address = ('127.0.0.1', 10000)

    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_TCP)

    print('connecting to {0} port {1}'.format(*address), file=log_buffer)

    sock.connect(address)
    buffer_size = 16
    received_message = ''

    try:
        print('sending "{0}"'.format(msg), file=log_buffer)
        msg = msg.encode('utf8')
        sock.sendall(msg)

        amount_received = 0
        amount_expected = len(msg)

        while amount_received < amount_expected:

            chunk = sock.recv(buffer_size)

            if not chunk:
                break

            amount_received += len(chunk)
            print('received chunk "{0}"'.format(chunk.decode('utf8')),
                  file=log_buffer)

            received_message += chunk.decode('utf8')

            if len(chunk) < buffer_size:
                break

    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
    finally:
        sock.close()
        print('closing socket', file=log_buffer)
        return received_message


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage = '\nusage: python echo_client.py "this is my message"\n'
        print(usage, file=sys.stderr)
        sys.exit(1)

    msg = sys.argv[1]
    client(msg)
