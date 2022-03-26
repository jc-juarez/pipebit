# -------------------------------
# PipeBit
# 'bitpacksender.py'
# Author: Juan Carlos Juárez.
# Licensed under MPL 2.0.
# All rights reserved.
# -------------------------------

from xmlrpc.client import Boolean
import pipebit.initial_config as initial_config
import sys
import random
import string
import threading
import time
from collections import deque

class SafeSender:

    # Standard Attributes

    pipeline_name = ""
    pipeline_path = ""
    pipeline_data_delimeter = "_%_"
    pipeline_debugging_option = 1
    pipeline_thread = ""

    # Memory & Caching Attributes

    send_packet_queue = deque()

    def __init__(self, _name, _debugging_option):

        # Invocation Thread Catching

        self.pipeline_thread = threading.currentThread()

        # Standard Attributes Initilization

        if(_name == ""):
            print("\n<#> PipeBit Error: Pipeline Name cannot be empty.\n")
            sys.exit(1)
        if(_debugging_option != 1 and _debugging_option != 0):
            print("\n<#> PipeBit Error: Debugging Option must be either 1 or 0.\n")
            sys.exit(1)
        self.pipeline_name = str(_name)
        self.pipeline_debugging_option = _debugging_option
        self.pipeline_path = str(initial_config.set(self.pipeline_name, self.pipeline_debugging_option, self.pipeline_data_delimeter))

        # Send Packet Queue Dispatcher thread

        send_packet_queue_dispatcher_thread = threading.Thread(target=self.send_packet_queue_dispatcher, name="SendQueueDispatcher", args=[0])
        send_packet_queue_dispatcher_thread.start()

        if(self.pipeline_debugging_option): print("\n<+> PipeBit Info: The BitPack Sender Pipeline '{0}' has been created succesfully.\n".format(str(self.pipeline_name)))

    def send(self, data): self.send_packet_queue.append(data)

    def send_function(self,data):
        # Sleep is Thread-Oriented. This will not slow down the main program but instead just this single thread for sending data through the pipeline
        time.sleep(0.3)   
        # Generate 16-character Transaction    
        transaction = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(16))
        packet = str(transaction) + "\n"
        for arg in data:
            packet += str(arg) + self.pipeline_data_delimeter
        binary_packet = bytes(packet, 'utf-8')
        with open(self.pipeline_path, "wb") as binary_file:
            binary_file.write(binary_packet)

    def send_packet_queue_dispatcher(self,args):
        while self.pipeline_thread.is_alive() or len(self.send_packet_queue):
            while(len(self.send_packet_queue)):
                self.send_function(self.send_packet_queue.popleft())
