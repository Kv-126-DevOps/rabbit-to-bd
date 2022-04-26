# Reabbit-to-Db

This application grabs data from RabbitMQ queue and saves to PostgreSQL database.

## Installation

### Create project folder
    cd ..
    sudo git clone -b develop https://github.com/Kv-DevOps-094/rabbit-to-bd.git
    cd rabbit-to-bd

### Create rabbit_to_postgres container
    sudo docker build -t rabbit_to_postgres .

### Run rabbit_to_postgres container
    sudo docker run -h rabbit_to_postgres --name rabbit_to_postgres --net bridge_issue -d -e POSTGRES_HOST=postgres -e POSTGRES_PORT=5432 -e POSTGRES_USER=issueuser -e POSTGRES_PW=Init1234 -e POSTGRES_DB=issuedb -e RABBIT_HOST=15.237.25.152 -e RABBIT_PORT=5672 -e RABBIT_USER=devops -e RABBIT_PW=softserve -e RABBIT_QUEUE=restapi rabbit_to_postgres