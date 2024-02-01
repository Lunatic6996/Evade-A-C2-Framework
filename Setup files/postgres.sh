#!/bin/bash

# Variables
PASSWORD="postgres"
DATABASE_NAME="e=Evade-C2" 

# Added the PostgreSQL repository
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

# Update system and install PostgreSQL
sudo apt update
sudo apt install -y postgresql postgresql-contrib

# Start and enable PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Set a password for the PostgreSQL user
sudo -u postgres psql -c "ALTER USER postgres PASSWORD '$PASSWORD';"

# Create a new PostgreSQL database
sudo -u postgres createdb $DATABASE_NAME

echo "PostgreSQL has been installed."
echo "PostgreSQL user password set to: $PASSWORD"
echo "New database created: $DATABASE_NAME"
