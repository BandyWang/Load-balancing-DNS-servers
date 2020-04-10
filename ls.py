import sys
import socket
import threading
import time

""" command line input: python ls.py <lsListenPort> <ts1Hostname> <ts1ListenPort> <ts2Hostname> <ts2ListenPort> """


class ThreadWithKill(threading.Thread):
    """
    The thread library provided by python does not have the option to cleanly kill threads, thus needing the use of a
    custom thread class that can be terminated by the parent via installing traces
    """
    def __init__(self, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.killed = False

    def start(self):
        self.__run_backup = self.run
        self.run = self.__run
        threading.Thread.start(self)

    def __run(self):
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, event, arg):
        if event == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, event, arg):
        if self.killed:
            if event == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True


def check_for_input_errors():
    if len(sys.argv) != 6:
        print("[ERROR] Incorrect number of command line arguments! Expected: 6, Received: {}".format(len(sys.argv)))
        return True
    return False


def establish_connection(hostname, port):
    try:
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.settimeout(5)
    except socket.error as err:
        exit()

    localhost_addr = socket.gethostbyname(hostname)
    server_binding = (localhost_addr, port)
    conn.connect(server_binding)
    return conn


def run_ls_server():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        exit()
    server_binding = ('', ls_listen_port)
    server.bind(server_binding)

    while True:
        print("[LS] Now listening for clients...")
        server.listen(1)
        csockid, addr = server.accept()
        print("[LS] Connected to client {}!".format(addr));
        while True:
            msg = csockid.recv(2048).decode()
            if msg:
                print("[LS] Received from client the following message: " + msg)
                results = [None]
                event = threading.Event()
                time_start = time.time()
                thread1 = ThreadWithKill(target=lookup, args=(ts1_hostname, ts1_listen_port, msg, results, event))
                thread1.start()
                thread2 = ThreadWithKill(target=lookup, args=(ts2_hostname, ts2_listen_port, msg, results, event))
                thread2.start()
                while not event.is_set():
                    time.sleep(0.001)

                if thread1.is_alive():
                    thread1.kill()
                if thread2.is_alive():
                    thread2.kill()
                time_end = time.time()
                total_time = time_end - time_start
                print("[LS] Replying to client with: {}. Total Time: {:.3f} seconds.".format(results[0], total_time))
                csockid.send(results[0])
            else:
                break


def lookup(hostname, listen_port, msg, buffer, event):
    # print("hostname:{} port:{} msg:{}".format('hostname', 'listenport', 'msg'))
    conn = establish_connection(hostname, listen_port)
    conn.sendall(msg.encode())
    while not event.is_set():
        try:
            buffer[0] = conn.recv(2048)
            event.set()
        except socket.timeout:
            buffer[0] = '- Error:HOST NOT FOUND'
            event.set()


if __name__ == "__main__":

    if not check_for_input_errors():
        ls_listen_port = int(sys.argv[1])
        ts1_hostname = sys.argv[2]
        ts1_listen_port = int(sys.argv[3])
        ts2_hostname = sys.argv[4]
        ts2_listen_port = int(sys.argv[5])

        run_ls_server()
