# Bombsweeper Bot

This is simple minesweeper-like Telegram game. 
You need to open all "free" squares and put flags on squares 
with bombs on them. If you open a cell with a bomb, the game is over.

## Used technology
* Python (tested with 3.9, should work on 3.7+);
* aiogram (Telegram Bot framework);
* Docker and Docker Compose (containerization);
* PostgreSQL (database);
* Redis (persistent storage for some ongoing game data);
* SQLAlchemy (working with database from Python);
* Alembic (database migrations made easy);
* Docker images are built with buildx for both amd64 and arm64 architectures.

## Installation

Create a directory of your choice. Inside it, make 3 directories for bot's data:  
`mkdir -p {pg-data,redis-data,redis-config}`

Grab `docker-compose-example.yml`, rename it to `docker-compose.yml` and put it next to your 
directories.

Grab `redis.example.conf` file, rename it to `redis.conf` and put into `redis-config` directory. 
Change its values for your preference.

Grab `env_dist` file, rename it to `.env` and put it next to your `docker-compose.yml`, open 
and fill the necessary data.

Finally, start your bot with `docker-compose up -d` command.
