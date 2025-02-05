# TEST TASK

Create FastAPI app with RabbitMQ to publish messages with different options.

## DEPENDENCIES

* docker compose

## INSTALL

* `cp .env.example .env`
* `docker compose up`

## Try it out

1. Send message to RabbitMQ

```
curl -X 'POST' \
  'http://localhost:8000/create-message' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "string"
}' ; echo
```

2. Send message with pause

```
curl -X 'POST' \
  'http://localhost:8000/create-message' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "string2",
  "deferance": 1
}' ; echo
```

3. Send periodic message with pause

```
curl -X 'POST' \
  'http://localhost:8000/create-message' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "string3",
  "deferance": 3,
  "periodic": true
}' ; echo
```
