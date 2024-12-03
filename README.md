# Spy Cat Agency

## Installing using GitHub
```shell
# clone the project and install the dependencies
git clone https://github.com/DSahalatyi/sca-test-task
cd sca-test-task
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# set environmental variables
set DJANGO_SECRET_KEY=<your secret key>
set POSTGRES_PASSWORD=<your db password>
set POSTGRES_USER=<your db user>
set POSTGRES_DB=<your db>
set POSTGRES_HOST=<your db host>
set POSTGRES_PORT=<your db port>
```
or configure `.env` file according to `.env.example`

## Run with docker
- Configure .env file according to .env.example
```shell
docker-compose build
docker-compose up
```

## Usage
[Postman collection](https://www.postman.com/aerospace-engineer-85956191/workspace/public/collection/24015896-0a33e100-7c79-4f64-b441-4ae7a2c7b973?action=share&creator=24015896)