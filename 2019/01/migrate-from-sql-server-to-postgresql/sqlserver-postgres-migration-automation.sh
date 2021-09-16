#!/bin/bash

# Pre-Requisite:
# Export tables(sql_server_schema) and views from SQL Server: all-tables-script-current.sql, all-views-script-current.sql
# Place data-integration.zip in a server to download quickly
# Generate Pentaho Data Migration Jobs and place in a server: migration-pdi-job.tar.gz
# Migrated Postgres functions in place: postgres-functions.sql and your-postgres-cleanup.sql

# Mandatory Initialization

DOMAIN='https://domain.com'
DB_NAME='database_name'
DB_USER='user_name'
DB_PASS='password'
DB_HOST='localhost'
DB_PORT='5432'

if [ -z "$DOMAIN" ] || [ -z "$DB_NAME" ] || [ -z "$DB_USER" ] || [ -z "$DB_PASS" ] || [ -z "$DB_HOST" ] || [ -z "$DB_PORT" ]; then
  echo 'ERROR : One or more variables are undefined'
  exit 1
fi


# Starting time
begin=$(date +"%s")

# tables schema migration
folder=`date +"%Y%m%d%H%M"`
mkdir -p /root/migration/$folder
cd /root/migration/$folder

wget $DOMAIN/all-tables-script-current.sql
git clone https://github.com/dalibo/sqlserver2pgsql.git

perl sqlserver2pgsql/sqlserver2pgsql.pl -f all-tables-script-current.sql -b all-tables-before.sql -a all-tables-after.sql -u all-tables-unsure.sql

sed -i 's/sql_server_schema/public/gI' all-tables-before.sql
sed -i 's/sql_server_schema/public/gI' all-tables-after.sql

rm -f all-tables-script-current.sql

# database setup

echo "$DB_HOST:$DB_PORT:$DB_NAME:$DB_NAME:$DB_PASS" >> ~/.pgpass
chmod 600 ~/.pgpass

sudo -u postgres -H -- psql <<EOF
SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = '$DB_NAME' AND pid <> pg_backend_pid();
DROP DATABASE $DB_NAME;
CREATE DATABASE $DB_NAME OWNER $DB_USER;
ALTER USER $DB_USER SET search_path TO public;
EOF

psql -U $DB_USER -p 5432 -h localhost -d $DB_NAME -qAt -f all-tables-before.sql

# Pentaho data integration setup

wget $DOMAIN/data-integration.zip
unzip data-integration.zip

mkdir -p ~/.kettle
echo "KETTLE_EMPTY_STRING_DIFFERS_FROM_NULL=Y" > ~/.kettle/kettle.properties

wget $DOMAIN/migration-pdi-job.tar.gz
tar -xzf migration-pdi-job.tar.gz
sed -i 's/<size_rowset>10000<\/size_rowset>/<size_rowset>100<\/size_rowset>/' migration-pdi-job/*

apt-get -y install default-jre

# Create tunnel to access SQL Server database through application server

echo "" >> ~/.ssh/config
cat <<EOT > ~/.ssh/config
Host production-server
    Hostname production-domain.com
    Port 22
    User root
    LocalForward 1433 <ip_address>:1433
EOT

ssh -M -S my-ctrl-socket -fnNT rt-prod-db
ssh -S my-ctrl-socket -O check rt-prod-db


job_name=`find migration-pdi-job/ | grep kjb`
./data-integration/kitchen.sh -file=$job_name -level=Basic | tee $folder.log

ssh -S my-ctrl-socket -O exit rt-prod-db


# views schema migration and functions setup

psql -U $DB_USER -p 5432 -h localhost -d $DB_NAME -qAt -f all-tables-after.sql

rm -f all-views-script-current.sql
wget $DOMAIN/all-views-script-current.sql

perl sqlserver2pgsql/sqlserver2pgsql.pl -f all-views-script-current.sql -b all-views-before.sql -a all-views-after.sql -u all-views-unsure.sql

sed -i 's/sql_server_schema/public/gI' all-views-unsure.sql
sed -i 's/[\[\]]//g' all-views-unsure.sql
# etc.

wget $DOMAIN/postgres-functions.sql

psql -U $DB_USER -p 5432 -h localhost -d $DB_NAME -qAt -f postgres-functions.sql
psql -U $DB_USER -p 5432 -h localhost -d $DB_NAME -qAt -c 'CREATE OPERATOR + (LEFTARG = varchar, RIGHTARG = varchar, PROCEDURE = concat_with_plus)'
psql -U $DB_USER -p 5432 -h localhost -d $DB_NAME -qAt -f all-views-unsure.sql

wget $DOMAIN/your-postgres-cleanup.sql
cp your-postgres-cleanup.sql /var/lib/postgresql/your-postgres-cleanup.sql
sudo -u postgres -H -- psql -d $DB_NAME -qAt -f /var/lib/postgresql/your-postgres-cleanup.sql

termin=$(date +"%s")
difftimelps=$(($termin-$begin))
echo "$(($difftimelps / 60)) minutes and $(($difftimelps % 60)) seconds elapsed for script execution."
