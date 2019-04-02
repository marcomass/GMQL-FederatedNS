# GMQL-Federated Name Server
The Name Server for GMQL-Federated provides name-resolution for federated datasets. Registered users can share their datasets with other users or groups of users. Moreover, the name server releases authentication tokens for comminication between two GMQL instances.

## Quick Start
Download this project and make sure that the <a href="https://docs.docker.com/v17.09/engine/admin/" target="_blank">docker daemon</a> is running on your machine. 

Go into the project directory and run the following script to start the name server:
```
sbin/start-nameserver
```
Use your favourite web-browser to access the web interface at port 8888 (e.g. if you run it locally: ht<span>tp</span>://localhost:8888/).

Stop the name server running the following script: 
```
sbin/stop-nameserver
```

## Requirements
### Running as a Django Application
Although this application is designed to run on a Docker container, you may run it as a normal Django application. 
In this case the requirements are:
- Python 2.7
- django
- djangorestframework 
- markdown 
- django-filter
- djangorestframework-xml
- sqlite3

### Running within Docker
In this case you just need to install Docker and start the Docker daemon.

## Deployment

### Running as a Django Application

The default location for the database file is the project folder. 
You can set a custom folder using the environment variable 'NAMESERVER_DB_PATH' with an absolute path.

Create the migrations: 
```
python manage.py makemigrations
```
Build the database:
```
python manage.py migrate
  ```
Start the application at localhost port 8800:
```
python manage.py runserver 0.0.0.0:8800
```

### Running within Docker
If you want to run the application within a Docker container, call the provided script:
```
sbin/start-nameserver [LOCAL-FOLDER] [PORT]
```
where `LOCAL-FOLDER` and `PORT` are two optional parameters:
- `LOCAL-FOLDER` : absolute path to the dabase folder in the local filesystem (by default the folder `data` automatically created in the working directory is used)
- `PORT` running port of the name server (default 8888)

Stop the name server running the following script:
```
sbin/stop-nameserver
```

## User Creation and API Authentication
### Admin Account
Admin priviledges are assigned to the first user that registers on the name server. 
### Registration and Login
Assuming the name server is running on `http://localhost:8888`, you can login and register a new user using the name server web interface:

- Open `http://localhost:8888/` in your browser and use the form to setup your account.


![signup](https://github.com/DEIB-GECO/GMQL-FederatedNS/raw/master/screenshots/signup.png)

![login](https://github.com/DEIB-GECO/GMQL-FederatedNS/raw/master/screenshots/login.png)



### Obtaining the API Token
The API token for your GMQL installation is displayed in the home page of the web interface after login.

![signup](https://github.com/DEIB-GECO/GMQL-FederatedNS/raw/master/screenshots/home.png)

## Setting up GMQL
In order to enable GMQL-Federated in your GMQL instance, add the following properties to your `repository.xml` file:
``` XML
    <property name="GF_ENABLED">true</property>
    <property name="GF_NAMESERVER_ADDRESS">http://..../</property>
    <property name="GF_INSTANCENAME">...</property>
    <property name="GF_TOKEN">...</property>
```

where: 
- `GF_ENABLED`: tells the syste whether to enable or disable GMQL-Federated  functionalities (default: `false`)
- `GF_NAMESERVER_ADDRESS`: the name server address (either the one provided by Politecnico di Milano or your own)
- `GF_INSTANCENAME`: the instance identifier that you use to login to the name server 
- `GF_TOKEN`: your API token

## Adding a Federated Dataset
The "Datasets" section of the name server allows users to share their public datasets with other members of the federation.

![dslist](https://github.com/DEIB-GECO/GMQL-FederatedNS/raw/master/screenshots/datasets-list.png)

Assuming that the logged user (instance) is "admin", the main page of this section will show a list of federated datasets that <i>admin</i> is allowed to use. <br>
These datasets can be:
- Datasets available to all the federation (i.e. shared with the group <i>GMQL-ALL</i>).
- Dataset owned by other members of the federation who have decided to share their dataset with <i>admin</i> or with a group of users (instances) that includes <i>admin</i>.
- Datasets created by "admin". In this case the dataset name will appear as a link, that, once clicked, allows the editing of that dataset.

In order to create a federated dataset, click on the "Add a new dataset" button. The dataset creation form will appear:

![dscreate](https://github.com/DEIB-GECO/GMQL-FederatedNS/raw/master/screenshots/datasets-creation.png)

The following fields are available: 
- <b>Name</b> (mandatory): name of the dataset, available in your public repository, that you want to add to the federation. The name written in this field must exactly match the name of the dataset in your public repository
- <b>Description</b>: a description of the dataset.
- <b>Privacy</b>: defines the instances (or groups of instances) that will be allowed to use your dataset. Choose among the instances (groups) in the left box and move them to the right box to allow them to use your dataset. By default, your instance is always allowed to see your datasets.
- <b>Repositories</b> : defines in which repositories (instances) the same dataset is available. By default your repository is added to this list. This feature is added to improve availability and performance of the system. For example, if you are running another instance of GMQL that has the same dataset in its public repository, you may add that instance in this list. If one of the instances in this list is offline, another instance in the list may be chosen for execution. Instances different from yours may be also chosen for optimization reasons. <u>Currently, GMQL-Federated does not support multiple repositories</u>.

  
## Groups 
The "Groups" section of the name server allows users to create groups of instances. Groups simplify the process of sharing a dataset with other members of the federation: as shown before, instead of defining the privacy of a dataset by sharing it with single instances, you may share it with a pre-defined group including multiple instances.

![gplist](https://github.com/DEIB-GECO/GMQL-FederatedNS/raw/master/screenshots/groups-list.png)

Assuming that the logged user (instance) is "admin", the main page of this section will show the list of groups having <i>admin</i> as a member. <br>
These groups can be:
- The group containing all instances in the federation (<i>GMQL-ALL</i>).
- Groups created by other members of the federation who have included <i>admin</i> as a member of the group.
- Groups created by <i>admin</i>. In this case the group name will appear as a link, that, once clicked, allows the editing of that group.

In order to create a group, click on the "Create a new group" button. The group creation form will appear:

![gpcreate](https://github.com/DEIB-GECO/GMQL-FederatedNS/raw/master/screenshots/groups-creation.png)

The following fields are available: 
- <b>Name</b> (mandatory): name of the group.
- <b>Instances</b> (at least two): members of the group.
  
Note that the creation of a group of instances does not imply that all instances in a group can use each other's datasets. The privacy of a dataset is always defined by the privacy list specified for that specific dataset.
  
  
