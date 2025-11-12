# \#rmaj-cis4160

## Setup

1. `npm install`
1. `npm start`

## Set Up Your Database

1. Start the Docker image: `docker-compose up`. Make sure you have Docker Desktop running.
1. `npm start`
1. Access `http://localhost:3000/users/`. If your data node is an empty array, you should populate your database.
1. Execute `curl -X POST localhost:3000/users/load-from-file` in the terminal.
1. Now refresh `http://localhost:3000/users/` and you should see a JSON blob for 5 users.