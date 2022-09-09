# PipeBit 🛸

PipeBit is a Quick Multi-Pipeline Deployment System for Local Data Pipelines based on Multi-Threading in Python without having to reference any pipeline paths.

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

PipeBit works on a Sender / Receiver model using Lists for both cases. Currently, PipeBit supports two Pipeline Models: **Safe Pipeline** and **Fast Pipeline**.

PipeBit can be used as a Multi-Pipeline system, having one Sender serving data over a specific Pipeline and having multiple Receivers extracting data from such Pipeline, allowing to create interesting data  transfer architectures.

## Safe Pipeline

This Model allows to safely transfer a data packet as a List, guaranteeing that it will be received by a Receiver if this last one is listening from the Pipeline. This model works on a Multi-Threading scheme having a Packet Queue on both sides so all packets are safely sent and received. 

**Use this Model when:**

- You need to transmit **important** and **small** amounts of data through the pipeline safely without losing any information. This Model can be good for event-driven notifications where everytime your program catches an event you can send information of about it through the Pipeline. An exmaple can be a program for checking a system's Health or any other case when you need to transmit few and relevant information. It is important to mention that this Model takes more time to send data than the **Fast Pipeline** model.

**Do Not Use this Model when:**

- You need to transmit **big** amounts of data in a **fast** manner as this Model is lengthier to transmit data. You can still transmit big amounts of data with this Model but it will take more time to receive it all. **It is not recommended** to use this Model in situations where data is sent sequentially indefinitely in a really short period of time (for instance a While True), but in case you decide to use it, be careful with the amounts of data you send and add time.sleep() intervals between each data packet you send, as the Packet Queue may be overloaded with huge amounts of data and may cause a Memory Leak problem on your server.

**SafeSender(name: str, debugging_option: int)**

This is the Object that creates the pipeline and takes in  parameters: the name the pipeline will have and the debugging option; if this last one is set to 1, PipeBt will show Debugging Information to the Console, otherwise if it is set to  it will not. PipeBit Errors will still be shown regardless of this option.

**send(data: List)**

This method sends a List as a Packet through the Pipeline.

**SafeReceiver(name: str, debugging_option: int)**

This Object only takes 1 parameter which is the name of the pipeline that is assumed to have already been created by a BitPackSender in the past. The Receiver works in an asynchronous way, as it starts to catch and save packets from the moment it is instantiated. No need to specify anything more, if the pipeline exists it will link it automatically. The Receiver Object works on a Multi-Thread Model, so it will begin to cache the incoming data from the pipeline since its declaration inside its packet cache memory.

**receive()**

This method of the object flushes the data from the packet cache memory and returns it as a List of Lists, where each of these Lists represents a packet that was sent over the pipeline since the Receiver first established a connection with the Pipeline.

Sender / Receiver Example
==========

For this example create two Python Files: **sender.py** and **receiver.py** and place them wherever you want, they don't need to be in the same directory nor anything. Here we check if the data received is not empty so we can display it.

It is recommended to use the **time** library if you pretend to send big amounts of data sequentially as in a While (True) statement so the Queue of Packets to be sent does not become too big and consume too much memory. For instance, you could use time.sleep(0.1) and it would work just fine.

Run both files parallelly, but first run the **sender.py** file so it creates the Pipeline (it will run and send all packets to the dispatcher and then the program will just wait for the dispatcher to finish) and then run the **receiver.py** file so it can extract the data coming from the Pipeline.

The content of the files is the following:

- sender.py

```python
import pipebit

# Defines SafeSender that creates a Pipeline with name 'data_pipe' with Debugging Information to Console
ss = pipebit.SafeSender("data_pipe",1)

# Iterates from 0 to 49 and sends the values from i, i + 1 ... i + 4 (size of 5)
for i in range(50):
    ss.send([i,i+1,i+2,i+3,i+4])

print("Finished! All Packets have been safely sent. Waiting for Packet Queue Dispatcher to Finish...")
```

- receiver.py

```python
import pipebit

# Defines SafeReceiver that connects with the Pipeline named 'data_pipe' with No Debugging Information to Console
sr = pipebit.SafeReceiver("data_pipe",0)

# Infinite Loop that listens for incoming data from the pipeline and prints it out to the console excepting an empty data value
while(True):
    data = sr.receive()
    if(len(data)):
        print(data)
```

Here is another example of **sender.py** using Tkinter to send the amount of times a Button is pressed, using the same **receiver.py** file as before and the same pipeline:

```python
from tkinter import *
import pipebit

# Define iterator starting at 1
i = 1

# Sends the Data to the Pipeline everytime the Button is pressed
def pressed_button(event):
    global i
    ss.send(["Pressed the button {0} times!".format(i)])
    i += 1  

# Create Button
widget = Button(None, text = "Send Data")
widget.pack()
widget.bind('<Button-1>', pressed_button)

# Create Clicks Pipeline
ss = pipebit.SafeSender("data_pipe",0)

# Tkinter Mainloop
widget.mainloop()
```
