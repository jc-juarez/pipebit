# -------------------------------
# PipeBit
# 'initial_config.py'
# Author: Juan Carlos Juárez.
# Licensed under MPL 2.0.
# All rights reserved.
# -------------------------------

import os
import sys
import inspect

def set(pipeline_name, pipeline_debugging_option, pipeline_data_delimiter):
    args = [pipeline_name, pipeline_debugging_option, pipeline_data_delimiter]
    pipebit_dir = str(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
    pipebit_path = repr(str(pipebit_dir))[1:-1]
    pipebit_pipelines_dir = "pipelines"
    pipebit_pipelines_path = os.path.join(pipebit_path, pipebit_pipelines_dir)
    if(not(os.path.isdir(pipebit_pipelines_path))):
        try:
            os.mkdir(pipebit_pipelines_path)
        except:
            print("\n<#> PipeBit Error: PipeBit Pipelines Directory cannot be found or created.")
            sys.exit(1)
    pipebit_current_pipeline_dir_path = os.path.join(pipebit_pipelines_path, pipeline_name)
    pipebit_current_pipeline_file_path = ""
    pipebit_current_pipeline_info_path = ""

    # Pipeline does not exist

    if(not(os.path.isdir(pipebit_current_pipeline_dir_path))):
        try:
            os.mkdir(pipebit_current_pipeline_dir_path)
        except:
            print("\n<#> PipeBit Error: Current Pipeline Directory cannot be created.")
            sys.exit(1)
        pipebit_current_pipeline_file_path = os.path.join(pipebit_current_pipeline_dir_path, pipeline_name)
        pipebit_current_pipeline_info_path = os.path.join(pipebit_current_pipeline_dir_path, "info.txt")
        try:
            with open(pipebit_current_pipeline_file_path, "wb") as pipeline_file:
                pass
        except:
            print("\n<#> PipeBit Error: Current Pipeline cannot be created.")
            sys.exit(1)
        try:
            with open(pipebit_current_pipeline_info_path, "w") as info_file:
                for arg in args:
                    info_file.write("{0}\n".format(str(arg)))
                info_file.write(pipebit_current_pipeline_file_path)
        except:
            print("\n<#> PipeBit Error: Current Pipeline Information File cannot be created.")
            sys.exit(1)
        return pipebit_current_pipeline_file_path

    # Pipeline Already exists

    pipebit_current_pipeline_file_path = os.path.join(pipebit_current_pipeline_dir_path, pipeline_name)
    pipebit_current_pipeline_info_path = os.path.join(pipebit_current_pipeline_dir_path, "info.txt")

    # Override Pipeline

    try:
        with open(pipebit_current_pipeline_file_path, "wb") as pipeline_file:
            if(pipeline_debugging_option): print("\n<+> PipeBit Info: [OVERRIDE] This Pipeline already exists. This Pipeline has been overriden. You can navigate to: '{0}' to delete the pipelines you no longer need.".format(str(pipebit_pipelines_path))) 
    except:
        print("\n<#> PipeBit Error: Current Pipeline cannot be created.")
        sys.exit(1)
    try:
        with open(pipebit_current_pipeline_info_path, "w") as info_file:
            for arg in args:
                info_file.write("{0}\n".format(str(arg)))
            info_file.write(pipebit_current_pipeline_file_path)
    except:
        print("\n<#> PipeBit Error: Current Pipeline Information File cannot be created.")
        sys.exit(1)
    return pipebit_current_pipeline_file_path