# Punk-Social

## About the project:
Punk Social is a simple social site used as a CRUD project demonstration. The
idea is to create groups within Punk Social, join groups, and post within these
groups with relevant information. One can only post in a group that they belong
to. Although this is true, all groups are public and all posts made by a user
can be seen on their profile page. The profile also displays groups that the user
has authored and joined. Only the group author can delete a group. Likewise, only
a post or comment author can delete their own content.

This project uses the Django user model and couples a separate created model
which allows the user to customize their profile including a profile picture,
user bio, and portfolio site link. Both generic class based views and custom
function views are used. Models are built using SQLite and views display SQLite
query skills. This project also uses features such as Bootstrap integration,
template inheritance, permissions based views, relative URL linking, and custom
form validation.

## Project Setup
To begin setting the project up the first step would be to clone the repository.
Once the repo is cloned, create a virtual environment, install the corresponding
dependencies and activate the environment.  This demo project is built using
Django 1.11.  To create the virtual environment I personally use conda environment
manager which can be applied using the following code. It's important to specify
the python version because the Django1.11 is compatible with python 3.5.

```sh
$ git clone https://github.com/mustardmann999/punk-social
$ cd punk-social

$ conda create --n myenv python==3.5.6
```

When conda asks you to proceed choose 'y'.
After creating the environment, activate it and install dependencies.

```sh
$ conda activate myenv

(env)$ pip install -r requirements.txt
```
The '(env)' means the environment has been activated. After installing the project
dependencies using 'requirements.txt', proceed by opening the punk-social folder
and use django's runserver command to initialize the locally hosted project and
navigate to 'http://127.0.0.1:8000/'.

```sh
(env)$ cd punk-social
(env)$ python manage.py runserver
```
Once the project is running and open on a browser, create a user profile, log in
and browse the basic CRUD functionality!
