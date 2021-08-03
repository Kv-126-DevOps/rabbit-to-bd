# Reabbit-to-Db

This application grabs data from RabbitMQ queue and saves to PostgreSQL database.

##Installation

###Create rabbit_to_postgres container
sudo docker build -t rabbit_to_postgres .

###Run rabbit_to_postgres container
sudo docker run -h rabbit_to_postgres --name rabbit_to_postgres --net bridge_issue -d --env-file=.env rabbit_to_postgres 