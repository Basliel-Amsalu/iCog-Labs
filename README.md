# Resume
in the resume.cypher there is a query to create a graph data of my resume and if you copy paste it in the neo4j browser or neo4j auraDB
and in the the resume_queries.cypher there are different queries to show different aspects of my resume
# Social network
this is a jupyter notebook that has different functions to perform different neo4j queries
and all these functions are used to build a flask api

The functions 
    - register_user
    - update_user
    - create_friendship
    - remove_friendship
    - send_friend_request
    - respond_to_friend_request
    - post
    - like_post
    - comment_on_post
    - create_group
    - join_group
    - friend_recommendation
    - search_user
all the above functions in a flask api in the handler functions 
these are the routes
  - http://localhost:8080/register
  - http://localhost:8080/update
  - http://localhost:8080/friend POST and DELETE
  - http://localhost:8080/sendrequest
  - http://localhost:8080/respondrequest
  - http://localhost:8080/post
  - http://localhost:8080/post/like
  - http://localhost:8080/post/comment
  - http://localhost:8080/group/create
  - http://localhost:8080/group/join
  - http://localhost:8080/friend/recommendation
  - http://localhost:8080/search
it runs on port 8080 for now but it can be changed in the run_server() function
in the notebook the last cells are there to run the api route handlers so that we can inspect the functions
