import sys
import socket

#  GLOBAL VARIABLES
HNS_FILEPATH = "PROJI-HNS.txt"
QUERIES = list()
OUTPUT_FILE = open("RESOLVED.txt", "w")

def check_for_input_errors():
    if len(sys.argv) != 3:
        print("[Error] Incorrect number of command line arguments!")
        return True
    return False


def populate_queries():
    try:
        fp = open(HNS_FILEPATH)
        line = fp.readline()
        while line:
            line = line.rstrip().lower()
            QUERIES.append(line)
            line = fp.readline()
    finally:
        fp.close()


def establish_connection(hostname, port):
    try:
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        exit()

    localhost_addr = socket.gethostbyname(hostname)
    server_binding = (localhost_addr, port)
    conn.connect(server_binding)
    return conn



def perform_queries(ls_conn):
    ## sends querys to lsServer
    ## writes result into resolved.txt



if __name__ == "__main__":
    if not check_for_input_errors():
        lsHostName = int(sys.argv[1])
        lsListenPort = int(sys.argv[2])

        populate_queries()
        rs_conn = establish_connection(lsHostName, lsListenPort)
        perform_queries(rs_conn)
        OUTPUT_FILE.close()