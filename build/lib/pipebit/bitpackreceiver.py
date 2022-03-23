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

def blocks(files, size=65536):
    while True:
        b = files.read(size)
        if not b: break
        yield b

class BitPackReceiver:

    # Standard Attributes

    pipeline_packet_size = 0
    pipeline_name = ""
    pipeline_path = ""
    pipeline_connection = False
    pipeline_data_delimeter = "_%_"
    pipeline_packet_delimeter = "/*/"

    # Memory & Caching Attributes

    packet_queue = deque()
    packets_cache_memory = []
    current_transaction = ""

    def __init__(self, _name):

        # Standard Attributes Initialization

        if(_name == ""):
            print("\n<#> PipeBit Error: Pipeline Name cannot be empty.")
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
        self.pipeline_packet_size = int(params[1])
        self.pipeline_data_delimeter = str(params[2])
        self.pipeline_packet_delimeter = str(params[3])
        self.pipeline_path = str(params[4])

        # Packet Catcher Thread Initialization

        packet_catcher_thread = threading.Thread(target=self.packet_catcher, name="PacketCatcher", args=[0])
        packet_catcher_thread.start()

        # Packet Queue Dispatcher Thread Initialization

        packet_queue_dispatcher_thread = threading.Thread(target=self.packet_queue_dispatcher, name="QueueDispatcher", args=[0])
        packet_queue_dispatcher_thread.start()

        print("\n<+> PipeBit Info: The BitPack Receiver Pipeline '{0}' has been created succesfully.".format(str(self.pipeline_name)))

    def open_connection(self):
        self.pipeline_connection = True

    def close_connection(self):
        self.pipeline_connection = False

    def receive(self):
        aux = self.packets_cache_memory
        self.packets_cache_memory = []
        return aux

    # Decoding Engine for Packet Threads
    def decoding_engine_entrance(self,args):
        packet = args.decode("utf-8").rstrip('\n')
        res = packet.split("_%_")
        res.pop()
        self.packets_cache_memory.append(res)

    # Packet Catcher Thread
    def packet_catcher(self,args):
        while True:
            try:
                with open(self.pipeline_path, "rb",encoding="utf-8",errors='ignore') as f:
                    number_lines = sum(bl.count("\n") for bl in blocks(f)) + 1
                    if(number_lines >= 3):
                        packet_transaction = ""
                        for line in f:
                            packet_transaction = line.decode("utf-8").rstrip('\n')
                            break
                        if(packet_transaction != self.current_transaction):
                            self.current_transaction = packet_transaction
                            self.packet_queue.append(f.readlines()[1])
            except:
                print("\n<#> PipeBit Error: Error on Catching Data from Pipeline '{0}'.".format(self.pipeline_name))


    # Safe Dispatcher Function. All packets that make it uo to here are already safely received
    def packet_queue_dispatcher(self,args):
        while True:
            while(len(self.packet_queue)):
                thread_code = random.randint(0,1000)
                packet_thread = threading.Thread(target=self.decoding_engine_entrance, name="DecodingEngineEntrance{0}".format(str(thread_code)), args=[self.packet_queue.popleft()])
                packet_thread.start()
                while(packet_thread.is_alive()):
                    pass
                 