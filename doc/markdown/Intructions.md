# Instructions

Aljuarismi understand the following order or instructions:

## Workspace functions

## Loading functions

### Load dataset

The following sentences are used during the training of Aljuarismi:

* load the dataset **Titanic**
* Load **Titanic**
* Open the dataset **Titanic**
* open **Titanic**
* load the dataset **titanic**.**csv**
* load **ecg**.**csv**
* open the dataset **energy**.**csv**
* open **clime**.**txt**

: load the dataset **Titanic**
Response: What is the file extension (txt, csv)?
: csv
Response: Where is it located?
:  /home/user/datasets/ -> (It will look for a file Titanic.csv in that folder)

 : load the dataset **Titanic**.**csv**
Response: Where is it located?
:  /home/user/datasets/ -> (It will look for a file Titanic.csv in that folder)


## Dataset management functions

## Change name

* rename **ecg** to **energy**
* rename **random0** to **random_0**
* change the name of **random0** into **rnd0_0**
* rename **titanic**

### Subset of dataset

#### \- By row

* select rows from energy starting at 1 until 10
* Get a subset of **energy** by rows
* Select a subset of **energy** by rows from **25** to **60**

#### \- By column

* Obtain a subset of **random0** by columns **col0**, **col1**, **col2** and **col5**
* Get a subset of **energy** by columns
* select columns **index** from **stomp0**
* get a subset of columns **col0**, **col5** and **col9** from **random1**
### Join of datasets

#### \- By row

* join by rows the datasets **energy** and **ecg**
* join **energy** and **ecg** by rows

#### \- By column

* Join by columns the datasets **energy** and **ecg**
* Join **energy** and **ecg** by columns

### Split of dataset

#### \- By row

* split **energy** by **20** rows
* split by rows the dataset **energy**
* split the dataset **energy** by **20** rows

#### \- By column

* split the dataset **energy** by **2** columns
* split by columns **energy**

## Dimensionality functions

* execute **visvalingam** for reducing **energy** to **40** points
* execute **ramerDouglasPeucker** on **energy** with an epsilon value of **0.5**
* execute **pip** for reducing **energy** to **50** points
* execute **paa** for reducing **energy** to **20** points
* apply **visvalingam** for reducing **energy** to **40** points
* apply **ramerDouglasPeucker** for reducing **energy** to **40** points
* apply **pip** for reducing **energy** to **40** points
* apply **paa** for reducing **energy** to **40** points

## Clustering functions

The following sentences are used during the training of Aljuarismi:

### Kmeans

* execute kmeans
* execute k-means
* apply kmeans to **Dataset**
* execute kmeans to **Dataset**

### Kshape

* execute kshape
* execute k-shape
* execute kshape with **10** clusters for **energy**
* execute kshape with **3** clusters for **energy** dataset
* apply kshape to **random1** with **5** clusters

## Features

* compute features on **energy**
* execute features on **energy**

##Library

### GetBackend
* get **backend**
* show the current **backend**
* get the current **backend**

###GetBackends
* get **backends**
* get all **backends**


###SetBackend
* set **CUDA** backend
* set **CPU** backend
* set  **opencl** backend

##Matrix

###Stomp
* execute **stomp** on **random2** and **random3** with subsequence length **10**
* execute **stomp** on **random1** and **random2** with subsequence length of **10**
* execute **stomp** for the datasets **random1** and **random2**
* execute **stomp** with **random2** and **random3** with subsequence length of **10**

##StompSelfJoin
* Execute **stomp** on **energy** with subsequence length of **20**
* Execute **stomp self join**  on **energy** with subsequence length of **3**
