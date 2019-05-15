# ECE 356 Project - Social Network (Using Python)

## Requirment

This project requires Python with version at least 3.5

Also, to connect MySQL, the mysql.connector will be needed.
To install mysql.connector, use

> $ pip install mysql-connector-python-rf

if you do not have pip, it can be installed by

> $ sudo apt install python3-pip

## Command-line Interfaces

The command to execute any function should be in the format of:

> $ python3 main.py [commandSwitch] [-argument_notation] [argument_value]

To show all the possible command types and the meaning of argument notations, using:

> $ python3 main.py -h

## SQL Configurations 

To connect to the local database, firstly, run the SQL code in the ``socialNetwork.sql`` on the local database, and then go to ``dbConnection.py`` file and update the configuration parameters to connect to the local database. The configuration format should look like following:

NOTE: database must match the DB name in ``socialNetwork.sql``

```
config = { 
  'user': 'user',
  'password': 'password',
  'host': '127.0.0.1',
  'database': 'SocialNetwork'
}
```

Alternatively, you can specify the SQL account you are using, by adding the user name and password to the commandline interface everytime, the format should be:

> $ python3 main.py -U sqlUserName -P sqlPassword

NOTE: the first method method is recommanded, otherwise you will need to include all the parameters every single time.

## Possible Commands

### Create User

To create a new user, use the command: 

> $ python3 main.py createUser -u userID -n firstName -l lastName -d dateOfBirth -R religion
-u: userID   
-n: first name of user  
-l: last name of user   
-d: birthday of user, in the format of 'yyyy-mm-dd'
-R: religion of user  

A sample has been showed below, the user with id david001, named David Dylan, was borned on Jan 25, 1990, and is a Christian.

> $ python3 main.py createUser -u david001 -n David -l Dylan -d 1990-01-25 -R Christianity

### Create Group

To create a new group, use the command:
-G: group name of the new added group
-m (optional): userIDs of the users will join the group (multiple)

> $ python3 main.py createGroup -G groupName [-m] [Members]

The example: user david001 and bob001 will be added into GroupA

> $ python3 main.py createGroup -G GroupA -m david001 bob001

### Create Topic

To create a new topic, use the command:
-t: the topic name of new created topic
-T: the parent topic name of the new added topic

> $ python3 main.py createTopic -t topic -T parentTopics

For example: topic soccer will be added under topic sports

> $ python3 main.py createTopic -t soccer -T sports

### User Add Post 

To add post as a user:
-u: userID of the user who made the post
-c: the content of the post
-t (optional): topics of the post (multiple)
-g (optional): the groupID if the post is only visible for the group members
-p (optional): the postID of the targeted post if the new post is a respose post to it

> $ python3 main.py insertPost -u userID -c content [-t] [topic[ topic ...]] [-g] [groupID] [-p] [postID]

For example:

> $ python3 main.py insertPost -u bob001 -c 'Hello world!' 

### User Join/Leave Group

To join a group for user:
-u: the userID
-g: the groupID that the user want to join

> $ python3 main.py joinGroup -u userID -g groupID

To leave a group:
-u: the userID
-g: the groupID that the user want to leave

> $ python3 main.py leaveGroup -u userID -g groupID

for example: 

> $ python3 main.py joinGroup -u bob001 -g 0

### User Follow/Unfollow User

To follow a user:  
-u: the userID  
-F: the userID of the user to be followed  

> $ python3 main.py followUser -u userID -F userID

To unfollow a user:   
-u: the userID  
-F: the userID of the user to be unfollowed  

> $ python3 main.py unfollowUser -u userID -F userID

### User Follow/Unfollow Topic

To follow a topic:  
-u: the userID  
-t: the topicName of the topic to be followed  

> $ python3 main.py followTopics -u userID -t topicName

To unfollow a topic:   
-u: the userID  
-t: the topicName of the topic to be unfollowed  

> $ python3 main.py unfollowTopics -u userID -t topicName


### React To Post

To mark a post as like/dislike/funny/sad  
-u: the userID  
-p: the postID you want to react with  
-r: the reaction type, which is string  
    "like"/"dislike"/"funny"/"sad"

> $ python3 main.py reactToPost -u userID -p postID -r reaction 

For example:

> $ python3 main.py reactToPost -u bob001 -p 2 -r 'like' 


### Check Post

To read the new posts  
-u: the userID  
-a (Optional): no parameters required, as long as this flag is set, all read/unread post for the user will be displayed. Defaultly only unread posts will be displayed  
-s (Opetional): check post from certain sources, post will filtered by "user" you followed, "topic" you followed, or the post in your "group". Deafaultly all of them are set on.  

> $ python3 main.py checkPosts -u userID [-a] [-s] ['source' ...] 

