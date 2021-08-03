# Reabbit-to-Db

This application grabs data from RabbitMQ queue and saves to PostgreSQL database.

##Installation

sudo docker build -t resrapi .

sudo docker run -h restapi --name restapi -d -p 5000:5000 --env-file=.env resrapi