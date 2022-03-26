# -------------------------------
# PipeBit
# 'bitpackreceiver.py'
# Author: Juan Carlos Juárez.
# Licensed under MPL 2.0.
# All rights reserved.
# -------------------------------

import os
import sys
import inspect
import threading
import random
from collections import deque
from xmlrpc.client import Boolean

class SafeReceiver:

    # Standard Attributes

    pipeline_name = ""
    pipeline_path = ""
    pipeline_data_delimeter = "_%_"
    pipeline_debugging_option = 1
    pipeline_thread = ""

    # Memory & Caching Attributes

    packet_queue = deque()
    packets_cache_memory = []
    current_transaction = ""

    def __init__(self, _name, _debugging_option):

        # Invocation Thread Catching

        self.pipeline_thread = threading.currentThread()

        # Standard Attributes Initialization

        if(_name == ""):
            print("\n<#> PipeBit Error: Pipeline Name cannot be empty.")
            sys.exit(1)
        if(_debugging_option != 1 and _debugging_option != 0):
            print("\n<#> PipeBit Error: Debugging Option must be either 1 or 0.\n")
            sys.exit(1)
        pipebit_dir = str(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
        pipebit_path = repr(str(pipebit_dir))[1:-1]
        pipebit_pipelines_dir = "pipelines"
        pipebit_pipelines_path = os.path.join(pipebit_path, pipebit_pipelines_dir)
        pipebit_current_pipeline_dir_path = os.path.join(pipebit_pipelines_path, _name)
        if(not(os.path.isdir(pipebit_current_pipeline_dir_path))):
            print("\n<#> PipeBit Error: Pipeline '{0}' does not exist.".format(_name))
            sys.exit(1)
        pipebit_current_pipeline_info_path = os.path.join(pipebit_current_pipeline_dir_path, "info.txt")
        if(not(os.path.isfile(pipebit_current_pipeline_info_path))):
            print("\n<#> PipeBit Error: Missing Information File for Pipeline '{0}'. Try to recreate the Pipeline Sender again.".format(_name))
            sys.exit(1)
        params = []
        with open(pipebit_current_pipeline_info_path, "r") as info_file:
            for line in info_file:
                params.append(line.rstrip('\n'))
        self.pipeline_name = str(params[0])
        self.pipeline_data_delimeter = str(params[2])
        self.pipeline_path = str(params[3])

        self.pipeline_debugging_option = _debugging_option

        # Packet Catcher Thread Initialization

        packet_catcher_thread = threading.Thread(target=self.packet_catcher, name="PacketCatcher", args=[0])
        packet_catcher_thread.start()

        # Packet Queue Dispatcher Thread Initialization

        packet_queue_dispatcher_thread = threading.Thread(target=self.packet_queue_dispatcher, name="QueueDispatcher", args=[0])
        packet_queue_dispatcher_thread.start()

        if(self.pipeline_debugging_option): print("\n<+> PipeBit Info: The BitPack Receiver Pipeline '{0}' has been created succesfully.".format(str(self.pipeline_name)))

    def receive(self):
        aux = self.packets_cache_memory
        self.packets_cache_memory = []
        return aux

    # Decoding Engine for Packet Threads
    def decoding_engine_entrance(self,args): 
        if(type(args) != str): 
            packet = args.decode("utf-8").rstrip('\n')
        else:
            packet = args
        res = packet.split("_%_")
        res.pop()
        self.packets_cache_memory.append(res)

    # Packet Catcher Thread
    def packet_catcher(self,args):
        while self.pipeline_thread.is_alive():
            try:
                with open(self.pipeline_path, "rb") as binary_file:
                    packet_transaction = ""
                    for line in binary_file:
                        packet_transaction = line
                        break
                    if(packet_transaction != self.current_transaction):
                        self.current_transaction = packet_transaction
                        packet = ""
                        for line in binary_file:
                            packet = line
                        self.packet_queue.append(packet)
            except:
                print("\n<#> PipeBit Error: Error on Catching Data from Pipeline '{0}'.".format(self.pipeline_name))

    # Safe Dispatcher Function. All packets that make it uo to here are already safely received
    def packet_queue_dispatcher(self,args):
        while self.pipeline_thread.is_alive() or len(self.packet_queue):
            while(len(self.packet_queue)):
                thread_code = random.randint(0,1000)
                packet_thread = threading.Thread(target=self.decoding_engine_entrance, name="DecodingEngineEntrance{0}".format(str(thread_code)), args=[self.packet_queue.popleft()])
                packet_thread.start()
                while(packet_thread.is_alive()):
                    pass
                 