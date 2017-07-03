# CaisseVL

CaisseVL is a very small cash registering software, used te register the sells of beer and burgers during small events.

It mainly focus on the ease of setup and use, not security.

<img src="https://user-images.githubusercontent.com/2883886/27782800-3e6311f8-5fd4-11e7-917d-b56f9d0b2e8a.png" width="100%"></img>

It is writen in [Python 3.4+](https://www.python.org/), with [Django Framework](https://www.djangoproject.com/) for backend.

# Hardware set-up

I will release a ready-to-use raspberry pi 3 image for server and client soon.

Wat will you need ?

For server :

* A Raspberry Pi 3 for server (or any other recent linux/debian based computer)

For each client :

* A raspberry pi 3, or any computer with a web brower
* A touch screen

For network :

You can connect the clients WiFi or wired connection, as you want.
No internet access is required on server or clients once in production.

# Installation

We will install caissevl and all dependencies in /opt/caissevl

All commands :

```sh
 sudo apt install python3-venv supervisor
cd /opt
sudo pyvenv-3.4 caissevl
chmod -R 777 caissevl
cd caissevl
mkdir logs
git clone https://github.com/Romular/caissevl.git
source bin/activate
pip install Django gunicorn
cd caissevl/caissevl
cp settings-dist.py settings.py
```

The only thing you may need to modify is the secret key

```sh
cd /opt/caissevl/caissevl
python manage.py migrate
python manage.py collectstatic
```

now, create a superuser

```sh
python manage.py chreatesuperuser
```

Enter the desired admin username, email and password

Create a new file, named gunicorn.sh in /opt/caissevl/bin :

```
#!/bin/bash
NAME="caissevl" # Name of the application
DJANGODIR=/opt/caissevl/caissevl # Django project directory
SOCKFILE=/opt/caissevl/caissevl/gunicorn.sock # we will communicte using this unix socket

USER=root # the user to run as
GROUP=root # the group to run as
NUM_WORKERS=5 # how many worker processes should Gunicorn spawn

MAX_REQUESTS=1 # reload the application server for each request
DJANGO_SETTINGS_MODULE=caissevl.settings # which settings file should Django use
DJANGO_WSGI_MODULE=caissevl.wsgi # WSGI module name

echo “Starting $NAME as `whoami`”

# Activate the virtual environment
cd $DJANGODIR
source /opt/caissevl/bin/activate

export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn’t exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn

# Programs meant to be run under supervisor should not daemonize themselves (do not use –daemon)
exec /opt/caissevl/bin/gunicorn ${DJANGO_WSGI_MODULE}:application --name $NAME --workers 5 --max-requests 1 --user=$USER --group=$GROUP --log-level=error --log-file=- -b 0.0.0.0:80
```

Create a conf for Supervisor

```
[program:caissevl]
command = /opt/caissevl/bin/gunicorn.sh
user = root
stdout_logfile = /opt/caissevl/logs/supervisor.log
redirect_stderr = true
environment=LANG=fr_FR.UTF-8,LC_ALL=fr_FR.UTF-8
```

You can of course change these settings according to your needs

Now start app :

```sh
sudo supervisorctl start caissevl
```

You can now connect to http://<ip_of_server>/admin/, and log on with your username and password

Add a category in the admin interface, then add articles to this category

Open http://<ip_of_server>/, and you will be able to add items to basket, and purchase orders.

Open http://<ip_of_server>/stats/ to see sums os sells and money gains

# TODO

* Show the last 3 commands of the curent cash register on the "Take Order" page
* More stats and graphs
* An admin must be able to add new items on menu
* An admin must be able to mark items as "Out of stock" so they can't be purchased, and are removed from the cash register
* Remove the "New Command" button, and replace with 2 buttons, "Cash" and "Credit card"
* Create a menu page, auto updated, with articles and categories that can be puchased, to show on TV screen
* Possibility for an admin to register cost prices, to calculate gross margin and earnings
