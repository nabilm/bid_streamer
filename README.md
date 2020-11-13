## A Demonstration of using FastAPI, Kafka , Faust and mongoDB
*A hope to aid some people who are new to those services and how to integrate them*

The integration consists of 5 microservices 


## Services
### Kakfa microservice 
which is a docker container that can be ready for production ( deploying on ECS for example ) where we will send our bid events

### Zookeeper
The needed service for kafka to work

### MongoDB
which is our app database

### bidder-api
see (bidder/README.md)

### bidder-streamer
see (bidder/README.md)


## How it works
- Creating users , items, events can be done through the API endpoints 
- Events are written to kafka topic
- Streamer process events from kafka topic and send it to mongodb for storage
- API connect to mongodb and query the data from users, items and events collection


## Flow
- Create a user 
- Create an item with an initial bid
- Create an event that has the user id and the item id created along with a bid value
- query user/users
- query item/items
- query user items
- query item bids

For complete example with swagger and post interface 

```bash
make up 
open http://localhost:8001/docs
```
This will display an interface which contain all info about the API and a way to try it each endpoint using a web based rest client


## Lunching locust tests
```bash
make test
open http://localhost:8089
```
You can hatch using number of simulate 2 and hatch rate of 1 to warm up
and then you can navigate to the stats of the tasks

`explore the data` you can use a client like https://robomongo.org/ which really good mongo client , mongo is exposed on mongodb://localhost:27017


## Requirements
All you need is 

- docker >=2.1.0.2
- docker-compose >= 1.24.1
- python 3.8

## Big thanks 
big thanks to https://github.com/wurstmeister/kafka-docker for the amazing work on kafka docker which i used in this example

## TODO 
- Unit tests to cover the code (pytest is in the requirements and now locust test are available)
- Use TDD in future work as it's proven to be really useful and faster in getting the big picture
- Instead of pin kafka-docker in the code use it as a vendor 
