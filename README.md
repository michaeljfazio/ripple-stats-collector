# Ripple Stats Collector

A prototype python script that collects statistics from a rippled server
and forwards them onto a REST endpoint. This code is intended to fulfill
the "Stats Collection" brief as detailed by the XRP Community Fund which
can be found [here](https://communityfund.xrptipbot.com/).

# Functional Description

In keeping with the XRP Community Fund brief the collection agent proposed 
here is a lightweight script with minimal dependencies. The script can be
scheduled to run periodically with a scheduling mechanism such as cron or
systemd. Stats collected by the script are consolidated into a single JSON
payload and signed using the local rippled validator key. The resulting
signature and payload are then forwarded to a REST service endpoint which is 
intended to be the "Stats Proxy & Validation" component as detailed by the
XRP Community Fund.

# Assumptions

1. The "Stats Proxy & Validation" service as detailed by the XRP Community Fund
    shall exist as a simple REST service that expects a POST request with a JSON
    body containing the collected stats and a header field containing the
    associated signature.
2. Signatures shall be generated using sign command of 
    [validator-keys tool](https://github.com/ripple/validator-keys-tool).

# Remaining Work

At this stage the code detailed here is just a proof-of-concept designed to
elicit feedback. However, it is the assertion of this author that the majority
of required functionality is implemented by this early version with minimal
effort remaining to complete. To be considered complete the following
should be added:

1. ~~Collection of OS stats not contained in rippled stats.~~ **Done!**
2. Appropriate installation and usage documentation.

# Requirements

1. Python
2. Pip

# Installing from Source

Checkout the code and run the following command.

```bash
python setup.py install
```

# Running the Prototype

In order to run the code you must be running a local rippled server or alternatively
use the Dockerfile contained in the root of the repository along with the following
commands to start one for test purpose.

```bash
docker build -t rippled .
docker run --name rippled rippled
```

The script currently assumes the former. If you choose the latter then
you will need to toggle the following code in the top portion of the script:

```python
# CMD_SIGN = "docker exec rippled /opt/ripple/bin/validator-keys sign %s"
# CMD_SERVER_INFO = "docker exec rippled rippled server_info"
# CMD_SERVER_STATE = "docker exec rippled rippled server_state"

CMD_SIGN = "/opt/ripple/bin/validator-keys sign %s"
CMD_SERVER_INFO = "rippled server_info"
CMD_SERVER_STATE = "rippled server_state"
```

Netcat can be used as a quick and dirty way to emulate the "Stats Proxy & Validation" 
service, as hypothesized in the assumption section detailed above.

```bash
nc -l 1234
```

The script assumes the proxy service is running on the local machine on port 1234 but
can be overridden using the "--proxy=<url>" option passed to the collect.py script.

Running the script then follows:

```bash
collect.py --proxy=http://localhost:1234
```

If you have correctly followed the above instructions, you should see something that
looks like the following:

```http
POST / HTTP/1.1
Host: localhost:1234
User-Agent: python-requests/2.21.0
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive
Digest: ECDSA=D5EF8F75D0559EA073D837B04979D168F9891A381702B2F85BB21E56DE54CD344A37C9018A0535FB3A90C42B2966695CA2872C1B4C7B5942D223C415BE3BE406
Content-Type: application/json
Content-Length: 5122

{"system": {"cpu": {"count": {"physical": 4, "logical": 2}, "freq": {"current": 2000, "min": 2000, "max": 2000}}, "mem": {"virt": {"total": 8589934592, "available": 2839642112, "used": 4950171648, "free": 15224832}, "swap": {"total": 2147483648, "used": 1232601088, "free": 914882560}}, "platform": "Darwin-18.6.0-x86_64-i386-64bit"}, "server_info": {"build_version": "1.3.1", "closed_ledger": {"age": 13, "base_fee_xrp": 1e-05, "hash": "696D513F8F3877FAC0861FED08587DE5A6E8EF22DA8346DDC74E8658380D44B6", "reserve_base_xrp": 200, "reserve_inc_xrp": 50, "seq": 437}, "complete_ledgers": "empty", "fetch_pack": 18904, "hostid": "cd2e6cc77ab3", "io_latency_ms": 1, "jq_trans_overflow": "0", "last_close": {"converge_time_s": 7.078, "proposers": 31}, "load": {"job_types": [{"avg_time": 2, "job_type": "untrustedProposal", "peak_time": 146, "per_second": 9, "waiting": 249}, {"in_progress": 1, "job_type": "ledgerData", "waiting": 18}, {"in_progress": 1, "job_type": "clientCommand"}, {"avg_time": 226, "job_type": "transaction", "over_target": true, "peak_time": 1578, "per_second": 14}, {"job_type": "batch", "peak_time": 1, "per_second": 7}, {"avg_time": 64, "job_type": "advanceLedger", "peak_time": 955, "per_second": 18}, {"avg_time": 168, "in_progress": 1, "job_type": "fetchTxnData", "peak_time": 5388, "per_second": 4, "waiting": 31}, {"avg_time": 44, "job_type": "writeAhead", "peak_time": 174}, {"avg_time": 574, "job_type": "trustedValidation", "over_target": true, "peak_time": 2226, "per_second": 8}, {"avg_time": 1, "job_type": "writeObjects", "peak_time": 28, "per_second": 7}, {"avg_time": 364, "job_type": "trustedProposal", "over_target": true, "peak_time": 1493, "per_second": 17}, {"in_progress": 1, "job_type": "sweep"}, {"job_type": "peerCommand", "peak_time": 108, "per_second": 690}, {"job_type": "diskAccess", "peak_time": 13, "per_second": 5}, {"job_type": "processTransaction", "per_second": 7}, {"job_type": "SyncReadNode", "peak_time": 62, "per_second": 35}, {"job_type": "AsyncReadNode", "peak_time": 91, "per_second": 721}, {"job_type": "WriteNode", "peak_time": 48, "per_second": 2}], "threads": 4}, "load_factor": 1, "peer_disconnects": "34", "peer_disconnects_resources": "0", "peers": 10, "pubkey_node": "n9KmRjsNNGtqMR18mJYJz4FbgFZ8K39vnSG5HAz166nYpfjtTCXh", "pubkey_validator": "none", "published_ledger": "none", "server_state": "connected", "server_state_duration_us": "486894676", "state_accounting": {"connected": {"duration_us": "2193214893", "transitions": 3}, "disconnected": {"duration_us": "56841752", "transitions": 3}, "full": {"duration_us": "0", "transitions": 0}, "syncing": {"duration_us": "0", "transitions": 0}, "tracking": {"duration_us": "0", "transitions": 0}}, "time": "2019-Aug-02 14:47:53.142138", "uptime": 2250, "validation_quorum": 25, "validator_list": {"count": 1, "expiration": "2019-Aug-14 00:00:00.000000000", "status": "active"}}, "server_state": {"build_version": "1.3.1", "closed_ledger": {"base_fee": 10, "close_time": 618072460, "hash": "696D513F8F3877FAC0861FED08587DE5A6E8EF22DA8346DDC74E8658380D44B6", "reserve_base": 200000000, "reserve_inc": 50000000, "seq": 437}, "complete_ledgers": "empty", "fetch_pack": 18904, "io_latency_ms": 1, "jq_trans_overflow": "0", "last_close": {"converge_time": 7078, "proposers": 31}, "load": {"job_types": [{"avg_time": 2, "job_type": "untrustedProposal", "peak_time": 156, "per_second": 2, "waiting": 286}, {"in_progress": 2, "job_type": "ledgerData", "waiting": 20}, {"avg_time": 751, "in_progress": 1, "job_type": "clientCommand", "peak_time": 2396, "waiting": 2}, {"avg_time": 120, "job_type": "transaction", "peak_time": 368, "per_second": 46}, {"job_type": "batch", "peak_time": 32, "per_second": 23}, {"avg_time": 274, "job_type": "advanceLedger", "peak_time": 1209, "per_second": 20}, {"avg_time": 286, "job_type": "fetchTxnData", "peak_time": 1033, "per_second": 42}, {"avg_time": 404, "job_type": "trustedValidation", "peak_time": 1271, "per_second": 7}, {"avg_time": 3, "job_type": "writeObjects", "peak_time": 54, "per_second": 8}, {"avg_time": 205, "job_type": "trustedProposal", "over_target": true, "peak_time": 853, "per_second": 12}, {"in_progress": 1, "job_type": "sweep"}, {"job_type": "peerCommand", "peak_time": 72, "per_second": 627}, {"avg_time": 2, "job_type": "diskAccess", "peak_time": 40, "per_second": 6}, {"job_type": "processTransaction", "peak_time": 5, "per_second": 23}, {"job_type": "SyncReadNode", "peak_time": 28, "per_second": 31}, {"job_type": "AsyncReadNode", "peak_time": 629, "per_second": 709}, {"job_type": "WriteNode", "peak_time": 2, "per_second": 12}], "threads": 4}, "load_base": 256, "load_factor": 625, "load_factor_fee_escalation": 256, "load_factor_fee_queue": 256, "load_factor_fee_reference": 256, "load_factor_server": 625, "peer_disconnects": "34", "peer_disconnects_resources": "0", "peers": 10, "pubkey_node": "n9KmRjsNNGtqMR18mJYJz4FbgFZ8K39vnSG5HAz166nYpfjtTCXh", "pubkey_validator": "none", "published_ledger": "none", "server_state": "connected", "server_state_duration_us": "491650939", "state_accounting": {"connected": {"duration_us": "2197971156", "transitions": 3}, "disconnected": {"duration_us": "56841752", "transitions": 3}, "full": {"duration_us": "0", "transitions": 0}, "syncing": {"duration_us": "0", "transitions": 0}, "tracking": {"duration_us": "0", "transitions": 0}}, "time": "2019-Aug-02 14:47:57.897337", "uptime": 2255, "validation_quorum": 25, "validator_list_expires": 619056000}}
```

Note that the body signature is specified by the 'Digest' header and follows the format 
ECDSA=SIGNATURE. The actual payload is first converted to base64 before being passed to
the validator-keys tool for signing. The receiving proxy must take this into account when
verifiying the signature.
