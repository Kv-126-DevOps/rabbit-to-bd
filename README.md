# Reabbit-to-Db

This application grabs data from RabbitMQ queue and saves to PostgreSQL database.

##Installation
sudo docker network create --driver bridge --subnet 10.0.1.0/24 --ip-range 10.0.1.0/24 bridge_issue

sudo docker run -h postgres --rm --name postgres --net bridge_issue -e POSTGRES_PASSWORD=password -e POSTGRES_USER=user -e POSTGRES_DB=db -e USERMAP_UID=999 -e USERMAP_GID=999 -d -p 5432:5432 -v $HOME/docker/volumes/postgres:/var/lib/postgresql/data postgres

sudo docker build -t resrapi .

sudo docker run -h restapi --name restapi --net bridge_issue -d -p 5000:5000 --env-file=.env resrapi