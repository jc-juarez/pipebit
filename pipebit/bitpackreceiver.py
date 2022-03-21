import os
import sys
import inspect

class BitPackReceiver:

    pipeline_packet_size = 0
    pipeline_name = ""
    pipeline_path = ""
    pipeline_connection = False
    pipeline_data_delimeter = "_%_"
    pipeline_packet_delimeter = "/*/"

    def __init__(self, _name):
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
        print("\n<+> PipeBit Info: The BitPack Receiver Pipeline '{0}' has been created succesfully.".format(str(self.pipeline_name)))

    def open_connection(self):
        self.pipeline_connection = True

    def close_connection(self):
        self.pipeline_connection = False

    def receive(self):
        res = []
        curr = ""
        with open(self.pipeline_path, "rb") as binary_file:
            for line in binary_file:
                curr = line.decode("utf-8")
        res = curr.split("_%_")
        res.pop()
        return res

                