# Elevator API

System for data consumption of ML systems

## INSTRUCTIONS TO CONFIGURATE PROJECT

``` bash
# Use compose file
export COMPOSE_FILE=local.yml

# Build docker container, install images and dependencies
docker-compose build

# Configurate djanngo database
docker-compose run --rm --service-ports django python manage.py makemigrations

docker-compose run --rm --service-ports django python manage.py migrate

# Run container
docker-compose up

```


### Upload elevator call data

To load the elevator call data contained in output.csv run the following command:

    $ python manage.py import_data
  
### Test coverage

  To run the tests:

    $ python manage.py test
