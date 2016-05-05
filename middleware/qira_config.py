import os
import sys


# Trace Libraries
TRACE_LIBRARIES = False

# Web Server
HOST = '0.0.0.0'
WEB_PORT = 3002
SOCAT_PORT = 4000
FORK_PORT = SOCAT_PORT + 1

# Use PIN
USE_PIN = False

# Temp Directories
if os.name == "nt":
    LOG_FILE_BASE = "c:/qiratmp/qira_log"
    ASM_FILE_BASE = "c:/qiratmp/qira_asm"
    TRACE_FILE_BASE = "c:/qiratmp/qira_logs/"
    GRAPH_FILE_BASE = "c:/qiratmp/qira_graph.png"
    BINARY_FILE_BASE = "c:/qiratmp/qira_binary"
    IN_DOT_FILE_BASE = "c:/qiratmp/qira_in.dot"
    OUT_DOT_FILE_BASE = "c:/qiratmp/qira_out.dot"
else:
    LOG_FILE_BASE = "/tmp/qira_log"
    ASM_FILE_BASE = "/tmp/qira_asm"
    TRACE_FILE_BASE = "/tmp/qira_logs/"
    GRAPH_FILE_BASE = "/tmp/qira_graph.png"
    BINARY_FILE_BASE = "/tmp/qira_binary"
    IN_DOT_FILE_BASE = "/tmp/qira_in.dot"
    OUT_DOT_FILE_BASE = "/tmp/qira_out.dot"

# Specify QIRA BASEDIR.
FILEDIR = os.path.realpath(
    os.path.dirname(os.path.realpath(__file__)))
BASEDIR = os.path.join(FILEDIR, "..")
sys.path.append(BASEDIR)

# New home of static2
sys.path.append(os.path.join(BASEDIR, "static2"))

# QIRA Directories
LIB_DIR = os.path.join(BASEDIR, "libs")
PIN_DIR = os.path.join(BASEDIR, "tracers", "pin")
QEMU_DIR = os.path.join(BASEDIR, "tracers", "qemu")
PIN_BINARY = os.path.join(PIN_DIR, "pin-latest", "pin")

# BAP is no longer supported
WITH_BAP = False

# TODO: Make this True in v3
# Static Engine
WITH_STATIC = False
STATIC_ENGINE = "builtin"

if os.name == "nt":
    STATIC_CACHE_BASE = "c:/qiratmp/qira_static_cache/"
else:
    STATIC_CACHE_BASE = "/tmp/qira_static_cache/"

# Enable WebSocket Debugging
WEBSOCKET_DEBUG = False
