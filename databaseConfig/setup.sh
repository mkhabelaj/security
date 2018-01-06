#!/bin/bash
#####################################################################################
##################################Setup postgres#####################################
#####################################################################################
# Ensure script runs in its intended directory
cd "$(dirname "$0")"
DATABASE=$1
PASSWORD=$2

if [[ -z ${DATABASE} ]] | [[ -z ${PASSWORD} ]]  ; then
        echo "One of you parameters are empty"
        exit 1;
fi



function create_config_table() {
    psql $1 < config.sql
}

# Check if postgres is installed
if  type psql >/dev/null 2>&1 ;
then
    echo 'POSTGRES is installed';
    # creating Database
    sudo -u ${USER} createdb ${DATABASE};
    echo 'creating the config table .....';
    create_config_table ${DATABASE};
else
    echo 'POSTGRES is installing';
    sudo apt-get install postgresql postgresql-server-dev-all;
    sudo -u postgres createuser ${USER};
    sudo -u postgres psql -c \
     "ALTER USER ${USER} WITH PASSWORD ${PASSWORD}'; ALTER USER${USER} WITH SUPERUSER;";
    sudo -u postgres createdb ${DATABASE};
    sudo service postgresql restart;
    echo 'creating the config table .....'
    create_config_table ${DATABASE};
fi

echo "Setup Database ${DATABASE} complete";


