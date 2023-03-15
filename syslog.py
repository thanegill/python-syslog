#!/usr/bin/env python

## Tiny Syslog Server in Python.

import socketserver
import argparse
import logging

parser = argparse.ArgumentParser()

parser.add_argument(
    "--debug",
    help="Set logging level to DEBUG.",
    action="store_const",
    dest="loglevel",
    const=logging.DEBUG,
    default=logging.INFO,
)

parser.add_argument(
    "--listen",
    help="Listen on address",
    default="0.0.0.0",
    dest="listen",
    action="store",
)

parser.add_argument(
    "--port",
    help="Listen on port",
    default=514,
    dest="port",
    action="store",
)

class SyslogUDPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = bytes.decode(self.request[0].strip())
        socket = self.request[1]
        logging.debug(f"Received {len(data)} bytes from {self.client_address[0]}")
        logging.info(f"{self.client_address[0]} {str(data)}")

if __name__ == "__main__":
    args = parser.parse_args()

    logging.basicConfig(
        level=args.loglevel, format="[%(asctime)s]: %(message)s")

    try:
        logging.info(f"Listening on UDP '{args.listen}:{args.port}'")
        server = socketserver.UDPServer((args.listen, args.port), SyslogUDPHandler)
        server.serve_forever(poll_interval=0.5)
    except (IOError, SystemExit):
        raise
    except KeyboardInterrupt:
        print("Crtl+C Pressed. Shutting down.")
