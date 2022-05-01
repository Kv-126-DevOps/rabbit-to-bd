# Rabbit-to-Db

This application grabs data from RabbitMQ queue and saves to PostgreSQL database.

## Installation

### Create infrastructure
    docker network create -d bridge kv126
    docker run --network=kv126 -d --name postgres -e POSTGRES_USER=dbuser -e POSTGRES_PASSWORD=dbpass postgres
    docker run --network=kv126 -d --name rabbit -e RABBITMQ_DEFAULT_USER=mquser -e RABBITMQ_DEFAULT_PASS=mqpass -p 15672:15672 rabbitmq:3.9-management

### Run rabbit-to-bd
    git clone --branch 1-rabbit-to-bd-code-refactoring https://github.com/Kv-126-DevOps/rabbit-to-bd.git /opt/rabbit-to-bd
    docker run --network=kv126 -e POSTGRES_HOST=postgres -e POSTGRES_PORT=5432 -e POSTGRES_USER=dbuser -e POSTGRES_PW=dbpass -e POSTGRES_DB=postgres -e RABBIT_HOST=rabbit -e RABBIT_PORT=5672 -e RABBIT_USER=mquser -e RABBIT_PW=mqpass -e RABBIT_QUEUE=restapi -d --name rabbit-to-bd -v /opt/rabbit-to-bd:/app python:3.9-slim sleep infinity
    docker exec rabbit-to-bd pip install -r /app/requirements.txt
    docker exec -d rabbit-to-bd bash -c "cd /app && python ./app.py"
