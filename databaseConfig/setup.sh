#!/bin/bash
#####################################################################################
##################################Setup postgres#####################################
#####################################################################################
# Check if postgres is installed
DATABASE=$1
if  type psql >/dev/null 2>&1 ;
then
    echo 'POSTGRES is installed';
else
    echo 'POSTGRES is installing';
    sudo apt-get install postgresql postgresql-server-dev-all;
    sudo -u postgres createuser ${USER};
    sudo -u postgres psql -c \
     "ALTER USER ${USER} WITH PASSWORD 'password'; ALTER USER${USER} WITH SUPERUSER;";
    sudo -u postgres createdb ${DATABASE};
    sudo service postgresql restart;
fi


