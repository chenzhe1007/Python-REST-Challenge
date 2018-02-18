
# Instructions
Fork this repository and submit a url to the forked repository with your solution.
Please provide documentation in this README explaining the following:
- How to run including any configuration needed
  since there is a mysql required, so i tried to bring up an composer that brings these two image together. the configuration of the server side running is in the Dockerfile, they can be changed as needed.
  
  python [-h] [-d] [-r] db_user db_pass db_host port file_path

  -d optional debugging mode, default to False
  -r optional empty any records pre-existing in the table on start of the server, default   
     True
  db_user required, user name of the database (in docker, root)
  db_host required, host name of the database (in docker, )
  db_pass required, password of the database (in docker, 871013)
  port to use running flask server
  file_path, file of csv, initial user list, (if user exist by providing duplicate id, the  
             record will be ignored with a warning)

  after setting up the parameter in Dockerfile, then cd into the directory where  
  Dockerfile and composer file, then run 
  
  docker-compose up   (this will pull a mysql 5.7 image and can be accessed by flask app)

- Any thoughts on how to expand this application in the future

  1. if turns out the read is far larger than writes, we can scale out with memcached  
  2. In the situation writes are continuously streaming in, we can set up an SQS as the
     middle buffer
  3. ideally, we could replace mysql with a column based or doc based db like Cassandra 
     for better file I/O
  4. since some of the query needs to retrieve all records, we can set up cache mechanism for longer duration for the past records. it will be extra beneficial if we don't support updates. then, we only load the data from db based on the last updated timestamp of the cached records and combine the results before response


- What you have covered or not covered.

1. what's covered:
   
   a. input validation/transformation, id duplicates, date value conversion
   b. persist the data by storing in a mysql db
   c. using flask cache module, the duration is set to be short.
   d. dockerized the app and backend and using composer to run

2. what's not covered:
   a. cassandra backend and potential cassandra cluster
   b. authentication on the api calls
   c. rate limiter on the api calls

## General instructions and tasks
Read and pull in data from people.csv.
Fill in the requests in server.py where TODOs are stated in the comments.
Get as many done as you can.
If you have time create unit tests.
Feel free to add other systems to the application.
Also feel free to submit issues on this public branch with questions if you have any.

