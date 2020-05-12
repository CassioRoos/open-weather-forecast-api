# Open-Weather-Forecast-API by Cassio Roos

## Objective

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

The dependencies are

```shell script
apispec==0.39.0
  - PyYAML [required: >=3.10, installed: 5.3.1]
flake8==3.7.9
  - entrypoints [required: >=0.3.0,<0.4.0, installed: 0.3]
  - mccabe [required: >=0.6.0,<0.7.0, installed: 0.6.1]
  - pycodestyle [required: >=2.5.0,<2.6.0, installed: 2.5.0]
  - pyflakes [required: >=2.1.0,<2.2.0, installed: 2.1.1]
PyJWT==1.6.4
pymongo==3.7.2
pytest-cov==2.5.0
  - coverage [required: >=3.7.1, installed: 4.4.2]
  - pytest [required: >=2.6.0, installed: 3.9.1]
    - atomicwrites [required: >=1.0, installed: 1.4.0]
    - attrs [required: >=17.4.0, installed: 18.2.0]
    - more-itertools [required: >=4.0.0, installed: 8.2.0]
    - pluggy [required: >=0.7, installed: 0.8.0]
    - py [required: >=1.5.0, installed: 1.7.0]
    - setuptools [required: Any, installed: 46.1.3]
    - six [required: >=1.10.0, installed: 1.12.0]
python-decouple==3.3
requests==2.21.0
  - certifi [required: >=2017.4.17, installed: 2018.10.15]
  - chardet [required: >=3.0.2,<3.1.0, installed: 3.0.4]
  - idna [required: >=2.5,<2.9, installed: 2.7]
  - urllib3 [required: >=1.21.1,<1.25, installed: 1.24.3]
tornado-swirl==0.1.16
  - tornado [required: >=5.1.1, installed: 6.0.3]

```

### Executing tests
To run the tests and coverage execute:

**MONGO NEEDS TO BE RUNNING TO RUN TESTS**

```shell script
pytest src/tests -v -s --cov=. --cov-report xml:coverage/coverage.xml --cov-report html:coverage_html --cov-report term-missing --cov-fail-under 90
```

The coverage is meant to break when is under 90%

### Docker environment

The app is using **python:3.7-slim** to build its image, and mongo version is **mongo:3.6**

A image of the application is necessary, to build this image run:

```shell script
docker build -t weather-forecast .
```

To run the compose, edit **docker-compose.yml** file inside the **docker** folder, and change the environment variables as you will, then run the command:
```shell script
docker-compose -f docker/docker-compose.yml up -d 
```
This will run all that you need to use the application.

##### Running separately
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

## Swagger
With the application running access the api endpoint **/swagger/spec.html**, like this [http://localhost:5001/swagger/spec.html](http://localhost:5001/swagger/spec.html) 

