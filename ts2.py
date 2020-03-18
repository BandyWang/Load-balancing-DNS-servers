import sys
import socket

TS_FILEPATH = "PROJI-DNSTS2.txt"
DNS_TABLE = dict()


def check_for_input_errors():
    if len(sys.argv) != 2:
        print("[ERROR] Incorrect number of command line arguments!")
        return True
    try:
        int(sys.argv[1])
    except ValueError:
        print("[ERROR] Expected valid integer as port number!")
        return True
    return False


def populate_DNS_table():
    try:
        fp = open(TS_FILEPATH)
        line = fp.readline()
        while line:
            line = line.rstrip()
            split = line.split(" ")
            DNS_TABLE[split[0].lower()] = [split[1], split[2]]
            if split[2] == 'NS':
                DNS_TABLE['NS'] = [split[0], 'NS']
            line = fp.readline()
    finally:
        fp.close()


def establish_server_and_serve(tsListenPort):
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        exit()
    server_binding = ('', tsListenPort)
    ss.bind(server_binding)

    while True:
        print("[TS] Now listening...")
        ss.listen(1)
        csockid, addr = ss.accept()
        print("[TS] Connected to client {}!".format(addr));
        while True:
            msg = csockid.recv(2048).decode()
            print("[TS] Recieved from client the following message: " + msg)
            if msg:
                if msg in DNS_TABLE:
                    reply = DNS_TABLE[msg][0] + " " + DNS_TABLE[msg][1]
                    print("[TS] Replying to client with: "+ reply)
                    csockid.send(reply)
                continue


if __name__ == "__main__":
    if not check_for_input_errors():
        populate_DNS_table()
        tsListenPort = int(sys.argv[1])
        establish_server_and_serve(tsListenPort)
