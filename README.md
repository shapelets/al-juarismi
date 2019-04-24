# ALJUARISMI

Aljuarismi is a chat assistant capable of executing time series analytics and plotting its results.
The main purpose of this chat bot is to provide a way to perform analytics in an easy and natural way.
It is a tool that helps to eliminate the programming barrier and to communicate with the machine in a 
natural manner. 

# Installation

Aljuarismo, requires the installation of [Khiva library](https://github.com/shapelets/khiva) and
[Khiva-python](https://github.com/shapelets/khiva-python) binding.

To install aljuarismi, just execute the following command from the root folder of the repo:

```
python setup.py install
```

It will install all libraries that are required to make aljuarismi work.

# Execution

To execute Aljuarismi, just execute the next command from the root folder of the repo:

```
python main.py
```

Note: To make it work, you must export the next environment variable with the path to a 
credentials file for dialogflow.
```
export GOOGLE_APPLICATION_CREDENTIALS=/absolute-path-to-file/aljuaritmo.json

```