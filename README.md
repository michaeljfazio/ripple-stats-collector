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

# Remaining Work

At this stage the code detailed here is just a proof-of-concept designed to
elicit feedback. However, it is the assertion of this author that the majority
of required functionality is implemented by this early version with minimal
remaining required effort to complete. To be considered complete the following
should be added:

1. Collection of OS stats not contained in rippled stats.
2. Appropriate installation and usage documentation.
3. Installers (RPM and DEB). Not technically necessary but potentially a good idea.

# Requirements

1. Python 3
2. Pip3

# Running the Prototype

In order to run the code you must be running a local rippled server or alternatively
you may use the Dockerfile contained in the root of the repository to start one for
test purpose. The script currently assumes the latter. If you choose the former then
you will need to toggle the following code in the top portion of the script:

```python
CMD_SIGN = "docker exec rippled /opt/ripple/bin/validator-keys sign %s"
CMD_SERVER_INFO = "docker exec rippled rippled server_info"
CMD_SERVER_STATE = "docker exec rippled rippled server_state"

# CMD_SIGN = "/opt/ripple/bin/validator-keys sign %s"
# CMD_SERVER_INFO = "rippled server_info"
# CMD_SERVER_STATE = "rippled server_state"
```

Netcat can be used as a quick and dirty way to emulate the "Stats Proxy & Validation" 
service, as hypothesized in the assumption section detailed above.

```bash
nc -l 1234
```

The script assumes the proxy service is running on the local machine on port 1234 but
can be overridden using the "--proxy=<url>" option passed to the collect.py script.

Run the script then follows:

```bash
./collect.py --proxy=http://localhost:1234
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

<COLLECTED STATS IN BODY>
```

Note that the body signature is specified by the 'Digest' header and follows the format 
ECDSA=SIGNATURE. This is easily extracted and verified by the proxy service.