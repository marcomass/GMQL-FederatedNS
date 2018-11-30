# GMQL-FederatedNS
The Nameserver for GMQL-Federated provides name-resolution for federated datasets. Registered users can share their datasets with otherusers or groups of users. Moreover, the nameserver releases authentication tokens for comminication between two GMQL instances.


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
python api/manage.py makemigrations
```
Build the database:
```
python api/manage.py migrate
  ```
Start the application at localhost port 8800:
```
python api/manage.py runserver 0.0.0.0:8800
```

### Running within Docker
If you want to run the application within a Docker container, call the provided script:
```
start-nameserver [LOCAL-FOLDER] [PORT]
```
where `LOCAL-FOLDER` and `PORT` are two optional parameters:
- `LOCAL-FOLDER` : absolute path to the dabase folder in the local filesystem (by default uses the folder `data` automatically created in the working directory)
- `PORT` running port of the nameserver (default 8888)

## User creation and API Authentication
### Admin account
Admin priviledges are assigned to the first user that registers on the nameserver. 
### Registration and login
Assuming the nameserver is running on `http://localhost:8888`, you can register a new user using the Django web rest UI:

- Open `http://localhost:8888/api/instance/` in your browser and use the form to setup your account.
- Once registered, use the login button in the top-right corner of the page to sign in. 
- After login you will be able to browse the whole UI (whose entry point is at: `http://localhost:8888/api/`).


### Obtaining the API Token
A registered user can retrieve his API token performing a `GET` call on his instance's entity: 
```
http://localhost:8888/api/instance/[INSTANCENAME]
```
Example answer:
``` HTML
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "instancename": "exampleinstance",
    "description": "Example User",
    "email": "example@polimi.it",
    "creation_date": "2018-11-29 14:02:02.454539+00:00",
    "location": "exampleinstance",
    "token": "XXXXXXXXXXXXXXX"
}
```

## Setting up GMQL
In order to enable GMQL-Federated in your GMQL instance, add the following properties to your `repository.xml` file:
``` XML
    <property name="GF_ENABLED">true</property>
    <property name="GF_NAMESERVER_ADDRESS">http://..../</property>
    <property name="GF_INSTANCENAME">...</property>
    <property name="GF_TOKEN">...</property>
```

where: 
- `GF_ENABLED`: tells the syste wheter to enable or disable GMQL-Federated  functionalities (default: `false`)
- `GF_NAMESERVER_ADDRESS`: the Nameserver address (either the one provided by Politecnico di Milano or your own)
- `GF_INSTANCENAME`: the instance identifier that you use to login to the nameserver 
- `GF_TOKEN`: your API token


