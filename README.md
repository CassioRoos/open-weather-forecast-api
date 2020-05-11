# Open-Weather-Forecast-API by Cassio Roos

##Objective

Tecnichal test using [OpenWeather API](https://home.openweathermap.org/).

### Installing dependencies
```shell script
pip install pipenv
```

In the root of the project run the command:
```shell script
# with pipenv
pipenv run python src\app.py
# without pipenv
python src\app.py
```

### Docker environment

A image of the application is necessary, to build this image run:

```shell script
docker build -t weather-forecast .
```

To run the compose, edit **docker-compose.yml** file inside the **docker** folder, and change the environment variables as you will, then run the command:
```shell script
docker-compose -f docker/docker-compose.yml up -d 
```
This will run all that you need to use the application.

#####Running separately
To run the application and the database separately, docker needs a network to connect the containers:

```shell script
docker network create app-forecast -d bridge
```
Then execute:

```shell script
#to run mongodb
docker-compose -f docker/docker-compose-mongo.yml up -d

#to run the app
docker-compose -f docker/docker-compose-app.yml up -d
```


##Swagger
With the application running access the api endpoint **/swagger/spec.html**, like this [http://localhost:5001/swagger/spec.html](http://localhost:5001/swagger/spec.html) 

