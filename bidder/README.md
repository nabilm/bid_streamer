# Bidder 

The bidder app is composed of two components ( Two microservices )

## API 

The API is build on ASYNCIO & Fast API 

The API 3 routes all routes reflect 3 models based on pydentic models user, item, event and each those model own a collection in mongodb

##**/users/**
 
 Where you can manage users, for this example i have create an API to create/get user/users/query users items ( bids ) and it reflect model user
 
 for more info have a look at (http://localhost:8001/docs#/users "Users API documentation ")


##**/items/**

Where you can Manage items create/get item/items , query bids on an item and it reflect model item

for more info have a look at (http://localhost:8001/docs#/items "Users API documentation ")

**Note that** : to get the winning bid in the time being for an item , you just need to 	query the item that has a field called winning bid , and this one is updating live through the streaming process


##**/events/**
And this where we can get events and create an event and it reflect model event

for more info have a look at (http://localhost:8001/docs#/events "Users API documentation ")

Note that for simplicity and time constrain i didn't implement pagination it's really needed for the api endpoints that get all users , items and events

####The API is using # Bidder 

The bidder app is composed of two components ( Two microservices )

## API 

The API is build on ASYNCIO & Fast API 

The API 3 routes 

##**/users/**
 
 Where you can manage users, for this example i have create an API to create/get user/users/query users items ( bids ) and it reflect model user
 
 for more info have a look at (http://localhost:8001/docs#/users "Users API documentation ")


##**/items/**

Where you can Manage items create/get item/items , query bids on an item and it reflect model item

for more info have a look at (http://localhost:8001/docs#/items "items API documentation ")

**Note that** : to get the winning bid in the time being for an item , you just need to 	query the item that has a field called winning bid , and this one is updating live through the streaming process


##**/events/**
And this where we can get events and create an event and it reflect model event 

for more info have a look at (http://localhost:8001/docs#/events "events API documentation ")

Note that for simplicity and time constrain i didn't implement pagination it's really needed for the api endpoints that get all users , items and events

###The swagger documentation contain all the schema , models and example values
###All API's will be tested through locust framework which will work as an integration test as well performance metric which is scalable as well it entirely based on typing and asyncIO
####The swagger documentation contain all the schema , models and example values
####All API's will be tested through locust framework which will work as an integration test as well performance metric


## Streamer

The streamer is built on Faust & AsyncIO

Events are written to a Kafka topic in the events APIs and the streamer stream the data from Kafka to mongodb , i had this component to make the solution more performant , scalable as well and flexible to any/multiple data storage syncs, so by that i can have the solution flexible to support for example an app database and analytics database as well

We can have also the flexibility to have a pipeline applied on the event before sending it to the database , we can even send the streamed event to another kafka topic which can be consumed by other backends

also it gives many chances of apply machine learning algorithms on during the stream processing ( some idea : https://towardsdatascience.com/how-to-build-a-real-time-fraud-detection-pipeline-using-faust-and-mlflow-24e787dd51fa )

and i tried hard to not tie the solution to mongodb objectID so i use UUID instead

There a demonstration of streaming invalid events to another topic , directly to db, update a record based on item change log by using faust table
