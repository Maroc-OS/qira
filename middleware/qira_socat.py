import os
import socket
import signal

import qira_config


BOUND_PORTS = {}


def get_next_run_id():
    ret = -1
    for i in os.listdir(qira_config.TRACE_FILE_BASE):
        if "_" in i:
            continue
        ret = max(ret, int(i))
    return ret + 1


def start_bindserver(program, port, parent_id, start_cl, loop=False):
    if port not in BOUND_PORTS:
        myss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        myss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        myss.bind((qira_config.HOST, port))
        myss.listen(5)
        BOUND_PORTS[port] = myss
    else:
        myss = BOUND_PORTS[port]

    if os.fork() != 0:
        return
    # bindserver runs in a fork
    while True:
        print "**** listening on", myss
        (css, address) = myss.accept()

        # fork off the child if we are looping
        if loop:
            if os.fork() != 0:
                css.close()
                continue
        run_id = get_next_run_id()
        print "**** ID", run_id, "CLIENT", css, address, css.fileno()

        fd_css = css.fileno()
        # python nonblocking is a lie...
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
        try:
            import fcntl
            fcntl.fcntl(
                fd_css,
                fcntl.F_SETFL,
                fcntl.fcntl(
                    fd_css,
                    fcntl.F_GETFL,
                    0) & ~os.O_NONBLOCK)
        except ImportError as err:
            print "**** cannot import fcntl module.", err
        os.dup2(fd_css, 0)
        os.dup2(fd_css, 1)
        os.dup2(fd_css, 2)
        for i in range(3, fd_css + 1):
            try:
                os.close(i)
            except AttributeError as err:
                pass
        # fingerprint here
        program.execqira(["-qirachild", "%d %d %d" %
                          (parent_id, start_cl, run_id)], shouldfork=False)
