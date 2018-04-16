import socket
import select
import sys

HOST = "localhost"
PORT = 9898
ADDR = (HOST, PORT)
BUFSIZE = 1024

_current_in_list = [sys.stdin]

def prompt():
    sys.stdout.write('<You> ')
    sys.stdout.flush()

def gen_message(room_id, raw_message):
    return '<RID:{}>{}</RID:{}>'.format(room_id, raw_message, room_id)


def main():
    room_id = raw_input('<Room ID> ')

    client_socket = socket.socket()
    client_socket.settimeout(2)

    try:
        client_socket.connect(ADDR)
        _current_in_list.append(client_socket)

        # notify all room's user that new client is entered
        client_socket.send(gen_message(room_id, ''))
    except socket.error:
        print "Unable to connect"
        sys.exit()

    print 'Connected to remote host. Start sending messages'
    prompt()

    while True:
        rlist, wlist, xlist = select.select(_current_in_list, [], [])
        for sock in rlist:
            if sock is client_socket:
                message = sock.recv(BUFSIZE)
                if not message:
                    print '\nDisconnected from chat server.'
                    sys.exit()
                else:
                    sys.stdout.write(message)
                    prompt()
            else:
                raw_message = sys.stdin.readline()
                client_socket.send(gen_message(room_id, raw_message))
                prompt()


if __name__ == '__main__':
    main()
