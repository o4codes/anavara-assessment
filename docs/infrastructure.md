# INFRASTRUCTURE

The infrastructure was built to accomodate various design considerations, some of which are:

### Deployment and Scaling
The project was built with docker to allow for easy deployement and scaling. Docker allows us to properly
containerize our project, therefore managing all resources in a single container. To scale the app, several instance
of the containers can be spun up and down at will.

### Data Storage
The project is built to store data in a postgresql database. This allows for easy and secure data storage, and
easy querying of the data. A relational database was chosen due to the strong relationship between the data and
the user. SQL databases helps establish these relationships for easy mapping of data. Need may arise for addtional
data to be stored in JSON and this is why POSTGRESQL was chosen. POSTGRESSQL is capable of creating fields to store 
JSON data and not just store the data, it can also query keys and values in the JSON pretty quickly and efficient.
This feature might come handy in the future as more considerations is consideration for addition data fields.
