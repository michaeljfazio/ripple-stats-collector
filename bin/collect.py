#!/usr/bin/env python3

import os
import json
import base64
import requests
import argparse
import psutil
import platform

# CMD_SIGN = "docker exec rippled /opt/ripple/bin/validator-keys sign %s"
# CMD_SERVER_INFO = "docker exec rippled rippled server_info"
# CMD_SERVER_STATE = "docker exec rippled rippled server_state"

CMD_SIGN = "/opt/ripple/bin/validator-keys sign %s"
CMD_SERVER_INFO = "rippled server_info"
CMD_SERVER_STATE = "rippled server_state"

DEFAULT_PROXY = 'http://localhost:1234'

# Parse program arguments.
parser = argparse.ArgumentParser(description='Collects local rippled and OS info, signs and forwards to a remote stats proxy.')
parser.add_argument('--proxy', nargs='?', default=DEFAULT_PROXY, help='stats collector proxy endpoint (e.g. https://stats.xrptipbot.com:1234)')
args = parser.parse_args()

# Collect useful system information (CPU, MEM, OS)
cpu_freq = psutil.cpu_freq()
cpu_count_physical = psutil.cpu_count()
cpu_count_logical = psutil.cpu_count(logical=False)
mem_virtual = psutil.virtual_memory()
mem_swap = psutil.swap_memory()
platform = platform.platform()
system_info = {
    'cpu': {
        'count': { 'physical': cpu_count_physical, 'logical': cpu_count_logical },
        'freq': { 'current': cpu_freq.current, 'min': cpu_freq.min, 'max': cpu_freq.max }
    },
    'mem': {
        'virt': { 'total': mem_virtual.total, 'available': mem_virtual.available, 'used': mem_virtual.used, 'free': mem_virtual.free },
        'swap': { 'total': mem_swap.total, 'used': mem_swap.used, 'free': mem_swap.free }
    },
    'platform': platform
}
server_info = json.loads(os.popen(CMD_SERVER_INFO).read())['result']['info']
server_state = json.loads(os.popen(CMD_SERVER_STATE).read())['result']['state']
payload = json.dumps({ 'system': system_info, 'server_info': server_info, 'server_state': server_state }).strip()
encoded = base64.encodebytes(payload.encode())
signature = os.popen(CMD_SIGN % encoded).read().strip()

headers = { 
    'Digest': 'ECDSA=%s' % signature,
    'Content-Type': 'application/json'
    }

# POST the payload and signature (in header) to the proxy service
r = requests.post(args.proxy, data=payload, headers=headers)
exit(0 if forward() else 1)