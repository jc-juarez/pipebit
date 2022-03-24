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

class BitPackSender:

    # Standard Attributes

    pipeline_packet_size = 0
    pipeline_name = ""
    pipeline_path = ""
    pipeline_connection = False
    pipeline_data_delimeter = "_%_"
    pipeline_packet_delimeter = "/*/"

    # Memory & Caching Attributes

    send_packet_queue = deque()

    def __init__(self, _name, _packet_size, _override):

        # Standard Attributes Initilization

        if(_name == ""):
            print("\n<#> PipeBit Error: Pipeline Name cannot be empty.")
            sys.exit(1)
        if(_packet_size < 1):
            print("\n<#> PipeBit Error: Pipeline Packet Size must be at least 1.")
            sys.exit(1)
        if(type(_override) != Boolean):
            print("\n<#> PipeBit Error: Pipeline Override Parameter must be Boolean.")
            sys.exit(1)
        self.pipeline_packet_size = _packet_size
        self.pipeline_name = str(_name)
        self.pipeline_path = str(initial_config.set(_name, _packet_size, _override, self.pipeline_data_delimeter, self.pipeline_packet_delimeter))

        # Send Packet Queue Dispatcher thread

        send_packet_queue_dispatcher_thread = threading.Thread(target=self.send_packet_queue_dispatcher, name="SendQueueDispatcher", args=[0])
        send_packet_queue_dispatcher_thread.start()

        print("\n<+> PipeBit Info: The BitPack Sender Pipeline '{0}' has been created succesfully.".format(str(self.pipeline_name)))

    def open_connection(self):
        self.pipeline_connection = True

    def close_connection(self):
        self.pipeline_connection = False

    def send(self, data):
        if(len(data) != self.pipeline_packet_size): 
            print("\n<#> PipeBit Error: Packet Size is different from number of arguments in the passed data.")
            return
        if(not self.pipeline_connection):
            print("\n<#> PipeBit Error: Pipeline Connection is closed.")
            return
        thread_code = random.randint(0,1000)
        inter_thread = threading.Thread(target=self.inter_function, name="InterThread{0}".format(str(thread_code)), args=[data])
        inter_thread.start()
    
    def inter_function(self,data):
        time.sleep(0.4)
        self.send_packet_queue.append(data)

    def send_function(self,data):
        # Sleep is Thread-Oriented. This will not slow down the main program but instead just this single thread for sending data thorugh the pipeline
        time.sleep(0.3)   
        # Generate 16-character Transaction    
        transaction = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(16))
        binary_transaction = bytes(transaction + "\n", 'utf-8')
        with open(self.pipeline_path, "wb") as binary_file:
            binary_file.write(binary_transaction)
        for arg in data:
            arg = str(arg) + self.pipeline_data_delimeter
            binary_data = bytes(arg, 'utf-8')
            with open(self.pipeline_path, "ab") as binary_file:
                binary_file.write(binary_data)
        binary_packet_delimiter = bytes(self.pipeline_packet_delimeter + "\n&", 'utf-8')
        with open(self.pipeline_path, "ab") as binary_file:
                binary_file.write(binary_packet_delimiter)

    def send_packet_queue_dispatcher(self,args):
        while True:
            while(len(self.send_packet_queue)):
                self.send_function(self.send_packet_queue.popleft())
