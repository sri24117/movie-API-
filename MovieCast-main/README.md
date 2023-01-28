# Installing/Running django with mysql on Ubuntu

### Install Ubuntu packages
Run the below command in Terminal to install the basic Ubuntu dependencies needed to install Django and mysql.
```sh
sudo apt-get install -y libgl1-mesa-glx libegl1-mesa libxrandr2 libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6 wget
```

After running it, run the below command to verify all the packages are installed. It prints success in the last line if everything went as expected and you can move to next steps.

```sh
dpkg -S libgl1-mesa-glx libegl1-mesa libxrandr2 libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6 wget && echo "success" || echo "failed"
```


### Installing mysql server
Run the below commands to install mysql server on Ubuntu
```sh
sudo apt update
```
```
sudo apt install -y mysql-server
```
```
sudo systemctl start mysql.service
```
Run the below command to verify that the server is installed. It prints success in the last line if everything went as expected and you can move to next steps.

```
sudo service mysql status | grep "active (running)" && echo "success" || echo "failed"
```

Now open mysql configuration file using the below command
```
sudo gedit /etc/mysql/mysql.conf.d/mysqld.cnf
```

It opens a text editor. In the editor, you see the below line
```
[mysqld]
```

Add skip-grant-tables below it so that it looks like below.

```
[mysqld]
skip-grant-tables
```

Also find these two lines in the editor
```
bind-address		= 127.0.0.1
mysqlx-bind-address	= 127.0.0.1
```

and change them to below
```
bind-address		= 0.0.0.0
mysqlx-bind-address	= 0.0.0.0
```

After the changes, the file should look like this

```
......<some text>...... 

[mysqld]
skip-grant-tables

......<some text>......

bind-address		= 0.0.0.0
mysqlx-bind-address	= 0.0.0.0

......<some text>......
```
Now save the file and close the editor.

Run the below command to restart the mysql server

```
sudo service mysql restart
```

Run the below command to open mysql interactive shell. Press enter when it asks for password.

```
mysql -u root -p
```

It should open a mysql shell like below.

```
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql>
```

Run below commands in the shell. These will set the mysql root password to be sunshine9. You can choose a different password if you want. Try choosing one with atleast 8 characters and with atleast one character and number.

```
flush privileges;
```
```
use mysql;
```
```
create USER  'root'@'%' IDENTIFIED BY 'sunshine9';
```
```
update user set plugin="mysql_native_password" where user='root';
```
```
flush privileges;
```
```
alter USER 'root'@'localhost' IDENTIFIED BY 'sunshine9';
```
```
flush privileges;
```
```
exit;
```

Run the below command to open the mysql configuration file again.

```
sudo gedit /etc/mysql/mysql.conf.d/mysqld.cnf
```

Remove the below line we added above, and save and exit the editor

```
skip-grant-tables
```

Restart the mysql server using the below command

```
sudo service mysql restart
```

Run the below command to verify that the mysql server is setup and ready to use. It prints success in the last line if everything went as expected and you can move to next steps.

```
echo "use mysql;" | mysql -u root -pnavodaya9 && echo "success" || echo "failed"
```

Run the below command to create sample database mysqllearn that we can use later
```
echo "create database mysqllearn;" | mysql -u root -psunshine9
```

### Installing python
We will use conda virtual environments to run python programs.

Run below command to download anaconda. It downloads the anaconda package into file anaconda.sh

```
wget -O anaconda.sh https://repo.anaconda.com/archive/Anaconda3-2022.05-Linux-x86_64.sh
```

You can also download latest version of anaconda from https://www.anaconda.com/products/distribution . Please rename the downloaded file to be anaconda.sh to proceed with further installation steps.

Run the below command to verify that you have the anaconda installation package

```
ls anaconda.sh && echo "success" || echo "failed"
```

Run below command to install anaconda. It will prompt you to accept an agreement. Press yes/agree to accept. Press enter to choose default option if it asks you to choose anything else.

```
bash anaconda.sh
```

Run the below command to init anaconda in bash shell

```
~/anaconda3/bin/conda init bash
```

Now close the terminal and open a fresh terminal.
In the fresh terminal run the below command to create a new virtual environment myenv

```
conda create -n myenv python=3.9 anaconda -y
```

Run the below command to activate the myenv environment

```
conda activate myenv
```

Run the below command to verify you have correct virtual environment loaded for further use.
It prints success in the last line if everything went as expected and you can move to next steps.

```
echo $CONDA_DEFAULT_ENV | grep myenv && echo "success" || echo "failed"
```

### Installing Django
Open new Terminal and run the below command to activate myenv

```
conda activate myenv
```

Run below command to install Django

```
pip install Django
```

### Creating sample Django application
Open new Terminal and run the below command to activate myenv

```
conda activate myenv
```

Run the bwlow command to create template files of a new django application sampleapp

```
django-admin startproject sampleapp
```

It creates a folder sampleapp and places all the django server code files in it.
You can edit the files, add apis to it, write your own django code in it.

To run the django server, first change into the directory sampleapp by running below command

```
cd myapp/
```

And run the below command to run the django server
```
python manage.py runserver 0.0.0.0:7345
```

Open another terminal instance and run the below command to verify that the server is running as expected. It prints success in the last line if everything went as expected and you can move to next steps.

```
curl -X HEAD http://localhost:7345/ && echo "success" || echo "failed"
```

### Running Django
From now onwards, you need two terminal instances, one to run django server and another to test the APIs.
After making changes to server code, you can press Control+C to stop the django server and run the below command to start the server with updated code changes.

```
python manage.py runserver 0.0.0.0:7345
```

Also make sure whenever you open a new terminal instance, you have to run the below command to activate correct conda environment. Do not run any commands before running this.

```
conda activate myenv
```

In the second terminal instance you can run below commands to test APIs.

To make a HTTP GET api request to path /foobar, run the below command

```
curl -X HEAD http://localhost:7345/foobar
```

To make a HTTP POST api request to path /foobar with json data {"samplekey": "sample value"}, run the below command

```
curl -d '{"samplekey": "sample value"}' -X POST -H 'Content-Type: application/json' http://localhost:7345/foobar
```

To make a HTTP DELETE api request to path /foobar, run the below command

```
curl -X DELETE http://localhost:7345/foobar
```

### Using mysql server in Django code 

Install python mysql package by running the below command

```
pip install pymysql
```

To connect to mysql server find the DATABASES line in django settings.py, that looks like something like below.

```
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

Change the default database engine to be the installed mysql server by making DATABASES to be something like below.

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
	    'NAME': 'mysqllearn',
        'USER': 'root',
        'PASSWORD': 'sunshine9',
	    'HOST':'localhost',
        'PORT': '3306',
    }
}
```

Now you can add mysql code to django server and restart the server to test django with mysql.

