import sys
import socket

#  GLOBAL VARIABLES
import time

HNS_FILEPATH = "PROJ2-HNS.txt"
QUERIES = list()
OUTPUT_FILE = open("RESOLVED.txt", "w")

""" command line input : python client.py <lsHostname> <lsListenPort> """


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
    for query in QUERIES:
        print "[Client] Now querying: " + query
        time_start = time.time()
        ls_conn.sendall(query.encode())
        ls_reply = ls_conn.recv(2048)
        time_end = time.time()
        print "[Client] Result: {}. Total Time: {:.3f} seconds.".format(ls_reply, time_end - time_start)
        OUTPUT_FILE.write(query + " " + ls_reply + '\n')
    ls_conn.close()
    print("[Client] All queries completed! Please check RESOLVED.txt for validation.")


if __name__ == "__main__":
    if not check_for_input_errors():
        lsHostName = sys.argv[1]
        lsListenPort = int(sys.argv[2])

        populate_queries()
        ls_conn = establish_connection(lsHostName, lsListenPort)
        perform_queries(ls_conn)
        OUTPUT_FILE.close()
