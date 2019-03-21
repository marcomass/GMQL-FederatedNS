# GMQL-Federated Name Server
The Name Server for GMQL-Federated provides name-resolution for federated datasets. Registered users can share their datasets with other users or groups of users. Moreover, the name server releases authentication tokens for comminication between two GMQL instances.

## Quick Start
Download this project and make sure that the <a href="https://docs.docker.com/v17.09/engine/admin/" target="_blank">docker daemon</a> is running on your machine. 

Go into the project directory and run the following script to start the name server:
```
sbin/start-name server
```
Use your favourite web-browser to access the web interface at port 8888 (e.g. if you run it locally: http://localhost:8888/).

Stop the name server running the following script: 
```
sbin/stop-name server
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
Admin priviledges are assigned to the first user that registers on the nameserver. 
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


