#!/usr/bin/env python3

import os
import json
import base64
import requests
import argparse

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

server_info = json.loads(os.popen(CMD_SERVER_INFO).read())['result']['info']
server_state = json.loads(os.popen(CMD_SERVER_STATE).read())['result']['state']
payload = json.dumps({ 'info': server_info, 'state': server_state }).strip()
encoded = base64.encodebytes(payload.encode())
signature = os.popen(CMD_SIGN % encoded).read().strip()

headers = { 
    'Digest': 'ECDSA=%s' % signature,
    'Content-Type': 'application/json'
    }

# POST the payload and signature (in header) to the proxy service
r = requests.post(args.proxy, data=payload, headers=headers)

# Return 0 if everything went well. Otherwise 1.
exit(0 if r.ok() else 1)