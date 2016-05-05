import os
import sys


TRACE_LIBRARIES = False
HOST = '0.0.0.0'
WEB_PORT = 3002
SOCAT_PORT = 4000
FORK_PORT = SOCAT_PORT + 1
USE_PIN = False

if os.name == "nt":
    LOG_FILE_BASE = "c:/qiratmp/qira_log"
    TRACE_FILE_BASE = "c:/qiratmp/qira_logs/"
else:
    LOG_FILE_BASE = "/tmp/qira_log"
    TRACE_FILE_BASE = "/tmp/qira_logs/"

# Specify QIRA BASEDIR.
BASEDIR = os.path.realpath(
    os.path.dirname(os.path.realpath(__file__))+"/../")

sys.path.append(BASEDIR)

# BAP is no longer supported
WITH_BAP = False

# TODO: Make this True in v3
WITH_STATIC = False
STATIC_ENGINE = "builtin"

if os.name == "nt":
    STATIC_CACHE_BASE = "c:/qiratmp/qira_static_cache/"
else:
    STATIC_CACHE_BASE = "/tmp/qira_static_cache/"

# Enable WebSocket Debugging
WEBSOCKET_DEBUG = False
