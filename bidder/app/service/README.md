# Services 

This is an isolation layer to let the API's Backend ignostic 
so when we decide to user another/additonal sources i.e Storage or streaming component we can just modify the service classes ( for example : Getting data from mysql and mongo in the same call )
in the same time api can be versioned if we want to or use the same apis endpoints but we different service package

It will be also useful if we want to divide the code into more microservices or shared packages