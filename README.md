# python_fastapi_mqtt_example

This project demonstrates the integration of FastAPI with MQTT and encryption. It is designed for developers who are new to FastAPI, MQTT, and encryption concepts.

---

## Features

- FastAPI for building RESTful APIs
- MQTT integration using the `EMQX` library
- Example of publishing and subscribing to MQTT topics
- Docker and Docker Compose support for containerized deployment

---

## Prerequisites

- Python 3.7 or higher
- Docker and Docker Compose (optional for containerized setup)
- An MQTT broker (e.g., Mosquitto)

---

## Installation and Setup


You need to have docker  and docker compse to run this project. You can customize in .env for posgresql and envv

```sh 
docker-compose up -d 
```

Than create and environment 

```sh
python3 -m venv env
```
or
```sh
python -m venv env
```

than install the dependency 

```sh 
pip install -r requirements.txt

```


after that you can run the code with guvicorn 


```
uvicorn main:app --reload
```