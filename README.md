# Rabbit-to-DB

This application grabs data from RabbitMQ queue and saves to PostgreSQL database.
Starting of the application creates Postgres Database with fields:  Actions, IssueActions, IssueLabels, IssueStates, Issues, Labels, States, Users       

## Installation

### Prerequisites
    Installed:
      Postgres 
      RabbitMQ

### Create infrastructure
    docker network create -d bridge kv126
    docker run --network=kv126 -d --name postgres -e POSTGRES_USER=dbuser -e POSTGRES_PASSWORD=dbpass postgres
    docker run --network=kv126 -d --name rabbit -e RABBITMQ_DEFAULT_USER=mquser -e RABBITMQ_DEFAULT_PASS=mqpass -p 15672:15672 rabbitmq:3.9-management

### Running the application rabbit-to-db
    git clone --branch 1-rabbit-to-db-code-refactoring https://github.com/Kv-126-DevOps/rabbit-to-db.git /opt/rabbit-to-db
    docker run --network=kv126 -e POSTGRES_HOST=postgres -e POSTGRES_PORT=5432 -e POSTGRES_USER=dbuser -e POSTGRES_PW=dbpass -e POSTGRES_DB=postgres -e RABBIT_HOST=rabbit -e RABBIT_PORT=5672 -e RABBIT_USER=mquser -e RABBIT_PW=mqpass -e RABBIT_QUEUE=restapi -d --name rabbit-to-db -v /opt/rabbit-to-db:/app python:3.9-slim sleep infinity
    docker exec rabbit-to-db pip install -r /app/requirements.txt
    docker exec -d rabbit-to-db bash -c "cd /app && python ./app.py"
    
### Application Properties

Parameters are set as environment variables

| Parameter     |   Value     | 
|:--------------|:------------|
| POSTGRES_HOST |   postgres  | 
| POSTGRES_DB   |   postgres  | 
| POSTGRES_PORT |    5432     |
| RABBIT_HOST   |   rabbit    |
| RABBIT_PORT   |    5672     |
| RABBIT_QUEUE  |   restapi   |

### Testing
    Connect to the container with DB Postres, connect to DB:
      psql -d postgres -U dbuser -W
    Check if fields of the DB created:
      \dt+
    
    Connect to the container with RabbitMQ and check created queue:
      rabbitmqctl list_queues



