# Use the official MySQL image as base
FROM mysql:5.7

# Copy the SQL script to create the table into the container
ENV MYSQL_ROOT_PASSWORD='root_password'
ENV MYSQL_DATABASE='my_database'
ENV MYSQL_USER='my_user'
ENV MYSQL_PASSWORD='my_password'

# Enable to load data local infile
RUN set global local_infile=true;

# Exposing on port 5005
EXPOSE 5005

# Copy the SQL script to create the table into the container
COPY dane_satisfaction2.csv dane_satisfaction2.csv
COPY init.sql /docker-entrypoint-initdb.d/