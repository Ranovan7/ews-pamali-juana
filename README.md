# Early Warning System Pamali Juana using python flask

### Basics

1. Fork/Clone
1. Activate a virtualenv
1. Install the requirements

### Set Environment Variables

Create .env file using the format from .env-template

### Create DB

Create the databases in `psql`:

```sh
$ psql
# create database <db name>
# create user <user name> with encrypted password '<password>';
# grant all privileges on database <db name> to <user name>;
# \q
```

Create the tables and run the migrations:

```sh
$ flask create-db
```

### Create admin user

```sh
$ flask create-admin
```

### Run the Application

```sh
$ flask run
```

Access the application at the address [http://localhost:5000/](http://localhost:5000/)
