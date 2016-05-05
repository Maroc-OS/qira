#!/usr/bin/env python2.7
import os
import sys
import struct

import qira_config as CFG


IS_VALID = 0x80000000
IS_WRITE = 0x40000000
IS_MEM = 0x20000000
IS_START = 0x10000000
IS_BIGE = 0x08000000    # not supported
SIZE_MASK = 0xFF

if os.name == "nt":
    if CFG.TRACE_FILE_BASE is not None:
        LOGFILE = CFG.LOG_FILE_BASE
        LOGDIR = CFG.TRACE_FILE_BASE
    else:
        LOGFILE = "c:/qiratmp/qira_log"
        LOGDIR = "c:/qiratmp/qira_log/"
else:
    if CFG.TRACE_FILE_BASE is not None:
        LOGFILE = CFG.LOG_FILE_BASE
        LOGDIR = CFG.TRACE_FILE_BASE
    else:
        LOGFILE = "/tmp/qira_log"
        LOGDIR = "/tmp/qira_logs/"


def flag_to_type(ftt_flags):
    if ftt_flags & IS_START:
        typ = "I"
    elif (ftt_flags & IS_WRITE) and (ftt_flags & IS_MEM):
        typ = "S"
    elif not (ftt_flags & IS_WRITE) and (ftt_flags & IS_MEM):
        typ = "L"
    elif (ftt_flags & IS_WRITE) and not ftt_flags & IS_MEM:
        typ = "W"
    elif not (ftt_flags & IS_WRITE) and not ftt_flags & IS_MEM:
        typ = "R"
    return typ


def get_log_length(log_fd):
    try:
        log_fd.seek(0)
        dat = log_fd.read(4)
        return struct.unpack("I", dat)[0]
    except AttributeError:
        return None


def read_log(log_fd, seek=1, cnt=0):
    log_fd.seek(seek * 0x18)
    if cnt == 0:
        dat = log_fd.read()
    else:
        dat = log_fd.read(cnt * 0x18)

    ret = []
    for i in range(0, len(dat), 0x18):
        (rl_address, rl_data, rl_clnum, rl_flags) = struct.unpack(
            "QQII", dat[i:i + 0x18])
        if not rl_flags & IS_VALID:
            break
        ret.append((rl_address, rl_data, rl_clnum, rl_flags))

    return ret


def write_log(log_fn, dat):
    # untested
    sss = [struct.pack("I", len(dat)) + "\x00" * 0x14]
    for (wl_address, wl_data, wl_clnum, wl_flags) in dat:
        sss.append(
            struct.pack(
                "QQII",
                wl_address,
                wl_data,
                wl_clnum,
                wl_flags))
    log_fd = open(log_fn, "wb")
    log_fd.write(''.join(sss))
    log_fd.close()

if __name__ == "__main__":
    # standalone this can dump a log
    for (address, data, clnum, flags) in read_log(open(sys.argv[1])):
        print "%4d: %X -> %X  %X" % (clnum, address, data, flags)
