# PipeBit 🛸

PipeBit is a Quick Pipeline Management System for Local Data Pipelines in Python without having to reference any pipeline paths.

How to Install PipeBit
==========

*Requirements: 
- Python 3.6+ installed.

Make sure you have Python 3.6+ installed and run the following command in your terminal to install PipeBit:

For MacOS and GNU/Linux:

```python
pip3 install junipercs
```

For Windows:

```python
pip install junipercs
```

How to Run PipeBit
==========

PipeBit works on a Sender / Receiver model using Lists for both cases. Currently, PipeBit supports one Pipeline Model: **BitPack**. This Model allows to transfer a data packet with a predetermined packet size that refreshes the pipeline buffer every time a new packet is sent. 

## BitPackSender

**BitPackSender(name: str, size: int, override: boolean)**

This is the Object that creates the pipeline and takes in 3 parameters: the name the pipeline will have, the size for the packet of data it will transfer, and its override option. This last option is a Boolean that can be set to True in the case that if the pipeline already exists, we override it (change size and clean its previous buffer value). If set to False it will keep its previous buffer value until changed.

## BitPackReceiver

**BitPackSender(name: str)**

This Object only takes 1 parameter which is the name of the pipeline that is assumed to have already been created by a BitPackSender in the past. No need to specify anything more, if the pipeline exists it will link it automatically.

Sender / Receiver Example
==========






