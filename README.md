# PipeBit 🛸

PipeBit is a Quick Pipeline Management System for Local Data Pipelines in Python without having to reference any pipeline paths.

How to Install PipeBit
==========

*Requirements: 
- Python 3.6+ installed.

Make sure you have Python 3.6+ installed and run the following command in your terminal to install PipeBit:

For MacOS and GNU/Linux:

```python
pip3 install pipebit
```

For Windows:

```python
pip install pipebit
```

How to Run PipeBit
==========

PipeBit works on a Sender / Receiver model using Lists for both cases. Currently, PipeBit supports one Pipeline Model: **BitPack**. This Model allows to transfer a data packet with a predetermined packet size that refreshes the pipeline buffer every time a new packet is sent. 

## BitPackSender

**BitPackSender(name: str, size: int, override: boolean)**

This is the Object that creates the pipeline and takes in 3 parameters: the name the pipeline will have, the size for the packet of data it will transfer, and its override option. This last option is a Boolean that can be set to True in the case that if the pipeline already exists, we override it (change size and clean its previous buffer value). If set to False it will keep its previous buffer value until changed.

**send(data: List)**

This method of the object sends a List of the specified size of the packet.

**open_connection()**

Opens connection with the Pipeline.

**close_connection()**

Closes connection with the Pipeline.

## BitPackReceiver

**BitPackReceiver(name: str)**

This Object only takes 1 parameter which is the name of the pipeline that is assumed to have already been created by a BitPackSender in the past. No need to specify anything more, if the pipeline exists it will link it automatically.

**receive()**

This method of the object receives the data from the Pipeline and returns it as a List.

**open_connection()**

Opens connection with the Pipeline.

**close_connection()**

Closes connection with the Pipeline.

Sender / Receiver Example
==========

For this example create two Python Files: **sender.py** and **receiver.py** and place them wherever you want, they don't need to be in the same directory nor anything. Here we use the **time** library to make the process a little slower so it can be visible, but there is no need to use it. We also use a 'previous' value in **receiver.py** so we don't get the same value from the pipeline indefinitely.

Run both files parallelly, but first run the **sender.py** file so it creates the Pipeline (it will run in about 15 seconds to finish the for loop, run the other file before this time so you can appreciate the result) and then run the **receiver.py** file so it can extract the data coming from the Pipeline.

The content of the files is the following:

- sender.py

```python
import pipebit
import time

# Defines Sender with that created a Pipeline with name 'data_pipe', size 5 and no Override
sender = pipebit.BitPackSender("data_pipe",5,False)

# Opens Sender Connection with the Pipeline
sender.open_connection()

# Iterates from 0 to 29 and send the values from i, i + 1 ... i + 4, having an interruption interval between each of half a second
for i in range(30):
    sender.send([i,i+1,i+2,i+3,i+4])
    time.sleep(0.5)
    
# Closes Sender Connection with the Pipeline
sender.close_connection()
```

- receiver.py

```python
import pipebit

# Defines Receiver that connects with the Pipeline named 'data_pipe'
receiver = pipebit.BitPackReceiver("data_pipe")

# Previous Data
prev_data = []

# Current Data
data = []

# Opens Receiver Connection with the Pipeline
receiver.open_connection()

# Infinite Loop that listens for incoming data from the pipeline and print it out to the console
while(True):
    data = receiver.receive()
    if(data != prev_data):
        print(data)
        prev_data = data
        
# Closes Receiver Connection with the Pipeline (Unreachable)
receiver.close_connection()
```
