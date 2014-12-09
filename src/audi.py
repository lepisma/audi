"""
The main audi script
--------------------

The script works using arguments passed to it.
Based on them, it can either work as a sender (by playing data)
or a receiver by recieving audio from mic.
"""

import argparse
import audioconv

def send(file_name):
    """
    Sends the file using the helper functions
    """
    pass

def receive(file_name):
    """
    Receives the incoming data and store as `file_name`
    """
    pass

# Argument parsing
# ----------------
parser = argparse.ArgumentParser(description = "Sends or receive files via audio port")

parser.add_argument("file", help = "The name of the file to send/receive")

action_group = parser.add_mutually_exclusive_group()
action_group.add_argument("-s", "--send", help = "Sends the specified file", action = "store_true")
action_group.add_argument("-r", "--receive", help = "Receives data and saves to file", action = "store_true")

args = parser.parse_args()

if args.send:
    send(args.file)
elif args.receive:
    receive(args.file)
else:
    print("Specify the action. Run `audi.py -h` for help")
