from mysql.connector import Error as MySqlError
from mysql.connector import errorcode
import time
import datetime
import sys

cnx = None
cursor = None

def setCnxCursor(set_cnx):
    global cnx
    global cursor
    cnx = set_cnx
    cursor = cnx.cursor()


# Add new post and its corresponding data
def insert_post(userID, content, topics=[], groupID=None, responsePostID=None):

    postID = newPostID()
    if postID < 0:
        return -1
    if not isValidPost(userID, groupID, responsePostID):
        return -1
    if len(content) == 0:
        print("Error: Cannot create a post with no content")
        return -1


    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

    mySQLOperation = ("INSERT INTO Post "
              "(postID, timestamp, content) "
              "VALUES (%s, %s, %s);")
    mySQLParams = (postID, timestamp, content)

    # Insert new Post
    if execQuery(mySQLOperation, mySQLParams) != 0:
        return -1
    # cursor.execute(mySQLOperation, mySQLParams)

    mySQLOperation = ("INSERT INTO UserPost"
                    " (userID, postID)"
                    " VALUES (%s, %s);")
    mySQLParams = [userID, postID]
    if execQuery(mySQLOperation, mySQLParams) != 0:
        return -1

    if len(topics) > 0:
        mySQLOperation = ("INSERT INTO PostTopics"
                        " (postID, topicName)"
                        " VALUES")
        mySQLParams = []

        for topicName in topics:
            mySQLOperation += " (%s, %s),"
            mySQLParams.append(postID)
            mySQLParams.append(topicName)
            # data_postTopics = (postID, topic)
        mySQLOperation = mySQLOperation[:-1] + ";"

        # print(mySQLOperation)
        # print(mySQLParams)

        # Insert new PostTopics
        if execQuery(mySQLOperation, mySQLParams) != 0:
            return -1
        # cursor.execute(mySQLOperation, mySQLParams)

    if groupID is not None:
        mySQLOperation = ("INSERT INTO GroupPost"
                        " (postID, groupID)"
                        " VALUES (%s, %s);")
        mySQLParams = [postID, groupID]
        if execQuery(mySQLOperation, mySQLParams) != 0:
            return -1
        # cursor.execute(mySQLOperation, mySQLParams)

    if responsePostID is not None:
        mySQLOperation = ("INSERT INTO PostResponse"
                        " (responderPostID, respondedPostID)"
                        " VALUES (%s, %s);")
        mySQLParams = [postID, responsePostID]
        if execQuery(mySQLOperation, mySQLParams) != 0:
            return -1
        # cursor.execute(mySQLOperation, mySQLParams)

    return saveQueries()


# Generate postID for the new post
def newPostID():
    mySQLOperation = ("SELECT MAX(postID) FROM Post;")
    if execQuery(mySQLOperation) != 0:
        return -1
    currentMaxPostID = cursor.fetchone()[0]
    if currentMaxPostID is None:
        currentMaxPostID = -1
    return (currentMaxPostID + 1)


# Check if post is valid (excludes validity of user/group ID existing)
def isValidPost(userID, groupID=None, respondID=None):
    if groupID is not None or respondID is not None:
        mySQLOperation = ("SELECT groupID FROM UserJoins WHERE userID = %s;")
        mySQLParams = [userID]
        if execQuery(mySQLOperation, mySQLParams) != 0:
            return False
        userGroups = [row[0] for row in cursor.fetchall()]
        postGroupID = None

        # If user is not in the group with ID groupID
        if groupID is not None and all(groupID != userGroup for userGroup in userGroups):
            print("Error: Cannot post in group " + str(groupID) + " because user " + userID + " is not in this group.")
            return False

        if respondID is not None:
            mySQLOperation = ("SELECT groupID"
                            " FROM Post"
                            " LEFT OUTER JOIN GroupPost USING (postID)"
                            " WHERE postID = %s;")
            mySQLParams = [respondID]
            if execQuery(mySQLOperation, mySQLParams) != 0:
                return False

            results = cursor.fetchall()
            
            # If a post with ID respondID does not exist
            if len(results) == 0:
                print("Error: Post to respond to (ID=" + str(respondID) + ") does not exist.")
                return False
            
            # If user is not in the group that the reponded post is in
            postGroupID = results[0][0]
            if postGroupID is not None and all(postGroupID != userGroup for userGroup in userGroups):
                print("Error: Cannot respond to post " + str(respondID) + " as user " + userID + 
                " is not in group that post is in (ID=" + str(postGroupID) + ").")
                return False

            # If given groupID mismatches with reponded post's group ID
            if groupID is not None and respondID is not None and groupID != postGroupID:
                print("Error: Mismatching group to post in (ID=" + str(groupID) + ") and the group that the post to respond to is in (ID=" + str(postGroupID) + ").")
                return False
    return True


# Add user and group to UserJoinGroup relationship
def joinGroup(userID, groupID):

    if not checkUserExist(userID):
        print("Error: User does not exist.")
        return -1
    elif not checkGroupExist(groupID):
        print("Error: Group does not exist.")
        return -1

    mySQLOperation = ("INSERT INTO UserJoins"
                    "(userID, groupID)"
                    " VALUES (%s, %s);")
    mySQLParams = [userID, groupID]

    if execQuery(mySQLOperation, mySQLParams) != 0:
        return -1

    return saveQueries()

# Remove select user and group tuple from UserJoinGroup relationship
def leaveGroup(userID, groupID):
    if not checkUserExist(userID):
        print("Error: User does not exist.")
        return -1
    elif not checkGroupExist(groupID):
        print("Error: Group does not exist.")
        return -1

    mySQLOperation = ("DELETE FROM UserJoins"
                    " WHERE userID=%s AND groupID=%s ;")
    mySQLParams = [userID, groupID]

    if execQuery(mySQLOperation, mySQLParams) != 0:
        return -1

    return saveQueries()

# Add multiple topics for same user
def followTopics(userID, topics):
    rc = 0
    for topicName in topics:
        rc = followTopic(userID, topicName)
        if rc != 0:
            return rc
    return saveQueries()

# Add user and topic to UserFollowsTopic relationship
def followTopic(userID, topicName):
    if not checkUserExist(userID):
        print("Error: User does not exist.")
        return -1
    elif not checkTopicExist(topicName):
        print("Error: Topic does not exist.")
        return -1

    mySQLOperation = ("INSERT INTO UserFollowsTopic"
                    "(userID, topicName)"
                    " VALUES (%s, %s);")
    mySQLParams = [userID, topicName]

    if execQuery(mySQLOperation, mySQLParams) != 0:
        return -1

    # Do not commit here; commit in followTopics
    return 0

# Remove multiple topics from a user's topic follow list
def unfollowTopics(userID, topics):
    rc = 0
    for topicName in topics:
        rc = unfollowTopic(userID, topicName)
        if rc != 0:
            return rc
    return saveQueries()


# Remove selected user and topic from UserFollowsTopic relationship
def unfollowTopic(userID, topicName):
    if not checkUserExist(userID):
        print("Error: User does not exist.")
        return -1
    elif not checkTopicExist(topicName):
        print("Error: Topic does not exist.")
        return -1

    mySQLOperation = ("DELETE FROM UserFollowsTopic"
                    " WHERE userID=%s AND topicName=%s ;")
    mySQLParams = [userID, topicName]

    print('unfollowTopic: ' + mySQLOperation)
    print(mySQLParams)

    if execQuery(mySQLOperation, mySQLParams) != 0:
        return -1

    # Do not commit here; commit in unfollowTopics
    return 0

# Add users to UserFollowsUser relationship
def followUser(FollowerUserID, FollowedUserID):
    if not checkUserExist(FollowerUserID) or not checkUserExist(FollowedUserID):
        print("Error: User does not exist.")
        return -1

    mySQLOperation = ("INSERT INTO UserFollowsUser"
                    "(FollowerUserID, FollowedUserID)"
                    " VALUES (%s, %s);")
    mySQLParams = [FollowerUserID, FollowedUserID]

    if execQuery(mySQLOperation, mySQLParams) != 0:
        return -1
    
    return saveQueries()

# Remove selected users from UserFollowsUser relationship
def unfollowUser(FollowerUserID, FollowedUserID):
    if not checkUserExist(FollowerUserID) or not checkUserExist(FollowedUserID):
        print("Error: User does not exist.")
        return -1

    mySQLOperation = ("DELETE FROM UserFollowsUser"
                    " WHERE FollowerUserID=%s AND FollowedUserID=%s")
    mySQLParams = [FollowerUserID, FollowedUserID]

    if execQuery(mySQLOperation, mySQLParams) != 0:
        return -1
    
    return saveQueries()

# SELECT postID
# FROM (SELECT postID
#         FROM GroupPost AS GP
#         WHERE groupID = 1
#         UNION DISTINCT 
#         SELECT postID FROM PostTopics AS PT
#         WHERE topicName = 'soccer'
#         UNION DISTINCT
#         SELECT postID FROM UserPost AS UP
#         WHERE userID = 'alex001') AS AP
# LEFT OUTER JOIN ReadPost AS RP USING (postID)
# WHERE NOT EXISTS
#     (SELECT *
#     FROM ReadPost AS RP2
#     WHERE RP.userID = 'bob001');

def checkPosts(userID, showAll=False, source=["user", "group", "topic"]):
    if not checkUserExist(userID):
        print("Error: User does not exist.")
        return -1

    postList = getPostList(userID, showAll, source)
    if postList is None:
        return -1

    if not showAll:
        postList = getUnreadPosts(userID, postList)
        if postList is None:
            return -1

    postList = getUserGroupPosts(userID, postList)
    if postList is None:
        return -1

    rc = printPosts(userID, postList)
    if rc != 0:
        return -1

    rc = updateRead(userID, postList)
    if rc != 0:
        return -1

    return 0


def getPostList(userID, showAll, source):
    groups = getFullGroupJoinedList(userID)
    topics = getFullTopicFollowList(userID)
    follows = [userID] + getFullUserFollowList(userID)

    if len(groups) == 0 and len(topics) == 0 and "user" not in source:
        return []

    mySQLOperation = ("SELECT postID, timestamp FROM (")
    mySQLParams = []

    if "user" in source and len(follows) > 0:
        mySQLOperation += (" SELECT "
                        "DISTINCT postID FROM UserPost "
                        "WHERE ")
        for follow in follows:
            if follow == follows[0]:
                mySQLOperation += "userID = %s"
                mySQLParams.append(follow)
            else:
                mySQLOperation += " OR userID = %s"
                mySQLParams.append(follow)

    if "group" in source and len(groups) > 0:
        if "user" in source:
            mySQLOperation += " UNION DISTINCT"
        mySQLOperation += (" SELECT DISTINCT postID FROM GroupPost"
                        " WHERE")
        for group in groups:
            if group == groups[0]:
                mySQLOperation += " groupID = %s"
                mySQLParams.append(group)
            else:
                mySQLOperation += " OR groupID = %s"
                mySQLParams.append(group)

    if "topic" in source and len(topics) > 0:
        if "user" in source or ("group" in source and len(groups) > 0):
            mySQLOperation += " UNION DISTINCT"
        mySQLOperation += (" SELECT "
                        "DISTINCT postID FROM PostTopics "
                        "WHERE")
        for topic in topics:
            if topic == topics[0]:
                mySQLOperation += " topicName = %s"
                mySQLParams.append(topic)
            else:
                mySQLOperation += " OR topicName = %s"
                mySQLParams.append(topic)

    mySQLOperation += (") AS AP"
                    " INNER JOIN Post USING (postID)"
                    " ORDER BY timestamp")
    if showAll:
        mySQLOperation += " LIMIT 50"
    mySQLOperation += ";"

    if execQuery(mySQLOperation, mySQLParams) != 0:
        return None

    postList = [post[0] for post in cursor.fetchall()]
    return postList


def getUnreadPosts(userID, inPostList):
    if len(inPostList) == 0:
        return inPostList

    mySQLOperation = ("SELECT postID FROM ReadPost"
                    " WHERE userID = %s AND (")
    mySQLParams = [userID]
    for postID in inPostList:
        mySQLOperation += "postID = %s OR "
        mySQLParams.append(postID)
    mySQLOperation = mySQLOperation[:-4] + ");"

    if execQuery(mySQLOperation, mySQLParams) != 0:
        return None

    readPosts = [post[0] for post in cursor.fetchall()]
    postList = []

    for postID in inPostList:
        if postID not in readPosts:
            postList.append(postID)
    return postList


# Get all group ids that the selected user is in
# def getGroupsIncludeUser(userID, groupPostList):
def getUserGroupPosts(userID, inPostList):
    if len(inPostList) == 0:
        return inPostList

    mySQLOperation = ("SELECT postID, groupID FROM Post LEFT OUTER JOIN GroupPost USING (postID)"
                    " WHERE")
    mySQLParams = []
    for postID in inPostList:
        mySQLOperation += " postID = %s OR"
        mySQLParams.append(postID) 
    mySQLOperation = mySQLOperation[:-3] + ";"

    # print(mySQLOperation)
    # print(mySQLParams)

    if execQuery(mySQLOperation, mySQLParams) != 0:
        return -1

    groupPostList = cursor.fetchall()
    # postList = getGroupsIncludeUser(userID, groupPostList)

    mySQLOperation = ("SELECT groupID FROM UserJoins WHERE userID = %s;")
    mySQLParams = [userID]
    if execQuery(mySQLOperation, mySQLParams) != 0:
        return False
    userGroups = [row[0] for row in cursor.fetchall()]

    # If user is not in the group with ID groupID
    # if  all(groupID != userGroup for userGroup in userGroups):
        # return False
    postList = []

    for post_group_tuple in groupPostList:
        if post_group_tuple[1] is None or any(post_group_tuple[1] == userGroup for userGroup in userGroups):
            postList.append(post_group_tuple[0])
    
    return postList

# Mark the posts as readed for selected user
def updateRead(userID, postList):
    mySQLOperation = "SELECT postID FROM ReadPost WHERE userID = %s;"
    mySQLParams = [userID]


    if execQuery(mySQLOperation, mySQLParams) != 0:
        return -1
        
    readPosts = [postID[0] for postID in cursor.fetchall()]
    newPostList = []
    for post in postList:
        if post not in readPosts:
            newPostList.append(post)

    if len(newPostList) > 0:
        mySQLOperation = ("INSERT INTO ReadPost"
                        " (userID, postID)"
                        " VALUES ")
        mySQLParams = []
        for postID in newPostList:
            if postID == newPostList[0]:
                mySQLOperation += (" (%s, %s)")
                mySQLParams.append(userID)
                mySQLParams.append(postID)
            else:
                mySQLOperation += (", (%s, %s)")
                mySQLParams.append(userID)
                mySQLParams.append(postID)
        mySQLOperation += (";")

        print(mySQLOperation)
        print(mySQLParams)

        if execQuery(mySQLOperation, mySQLParams) != 0:
            return -1

    return saveQueries()


# Pretty Print the Posts
def printPosts(userID, postIDList, groupID=None, respondID=None):
    print("Posts for " + userID + " : \n")
    for postID in postIDList:
        mySQLOperation = ("SELECT firstName, lastName, content, timestamp, P.postID, groupName, groupID, respondedPostID"
                        " FROM Post AS P"
                        " INNER JOIN UserPost USING (postID)"
                        " INNER JOIN User USING (userID)"
                        " LEFT OUTER JOIN GroupPost USING (postID)"
                        " LEFT OUTER JOIN UserGroup USING (groupID)"
                        " LEFT OUTER JOIN PostResponse AS PR ON(P.postID = PR.responderPostID)"
                        " WHERE P.postID = %s")
        mySQLParam = [postID]
        if execQuery(mySQLOperation, mySQLParam) != 0:
            return -1

        results = cursor.fetchall()

        for (firstName, lastName, content, timestamp, postID, groupName, groupID, respondID) in results:
            mySQLOperation = ("SELECT reaction, COUNT(*) AS count"
                            " FROM Post"
                            " INNER JOIN Reaction USING (postID)"
                            " WHERE postID = %s"
                            " GROUP BY reaction;")
            mySQLParam = [postID]

            if execQuery(mySQLOperation, mySQLParam) != 0:
                return -1
            results = cursor.fetchall()
            reactionsCount = {
                "like" : 0,
                "dislike" : 0,
                "funny" : 0,
                "sad" : 0
            }
            for (reaction, count) in results:
                reactionsCount[reaction] = count

            mySQLOperation = ("SELECT topicName"
                            " FROM PostTopics"
                            " WHERE postID = %s;")
            mySQLParam = [postID]
            if execQuery(mySQLOperation, mySQLParam) != 0:
                return -1
            topicList = [row[0] for row in cursor.fetchall()]

            print ("=================================================\n")
            info = "{} {} (post ID {})".format(firstName, lastName, postID)
            if groupID is not None:
                info += " in {} ({})".format(groupName, groupID)
            if respondID is not None:
                info += " responding to " + str(respondID)
            print ("{} :".format(info))
            print ("Posted at : {}".format(timestamp))
            if len(topicList) != 0:
                print ("Topics : " + str(topicList))
            print ("| Like : {} | Dislike : {} | Funny : {} | Sad: {} |\n".format(reactionsCount["like"], reactionsCount["dislike"], reactionsCount["funny"], reactionsCount["sad"]))
            print ("{} \n".format(content))
    
    print ("=================================================\n")
    return 0


# Get all recursive subtopics of a list of topics the given user is follwing
def getFullTopicFollowList(userID):
    mySQLOperation = ("SELECT topicName FROM UserFollowsTopic"
                    " WHERE userID = %s;")
    mySQLParams = [userID]
    cursor.execute(mySQLOperation, mySQLParams)
    topics = []
    for topic in cursor:
        topics.append(topic[0])
    
    # Recuresivly get full list
    tmpList = [] + topics
    topicList = []
    topicCount = len(tmpList)

    # do (query sub topics) while (get new parent topics)
    while len(topics) != 0:
        mySQLOperation = ("SELECT subTopic FROM TopicRelation"
                        " WHERE")
        mySQLParams = []

        for topic in tmpList:
            if topic == tmpList[0]:
                if topic not in topicList:
                    topicList.append(topic)
                mySQLOperation += " parentTopic = %s"
                mySQLParams.append(topic)
            else:
                if topic not in topicList:
                    topicList.append(topic)
                mySQLOperation += " OR parentTopic = %s"
                mySQLParams.append(topic)
        mySQLOperation += ";"

        cursor.execute(mySQLOperation, mySQLParams)
        tmpList = []
        for subTopic in cursor:
            tmpList.append(subTopic[0])
        if len(tmpList) == 0:
            break

    # print("topicList: " + str(topicList))
    return topicList

# Get all people the user following
def getFullUserFollowList(userID):
    mySQLOperation = ("SELECT followedUserID FROM UserFollowsUser"
                    " WHERE followerUserID = %s;")
    mySQLParams = [userID]
    cursor.execute(mySQLOperation, mySQLParams)
    followList = []
    for FollowedUserID in cursor:
        followList.append(FollowedUserID[0])

    # print(followList)
    return followList


# Get all groups the user join in
def getFullGroupJoinedList(userID):
    mySQLOperation = ("SELECT groupID FROM UserJoins"
                    " WHERE userID = %s;")
    mySQLParams = [userID]
    cursor.execute(mySQLOperation, mySQLParams)
    joinList = []
    for groupID in cursor:
        joinList.append(groupID[0])

    # print(joinList)
    return joinList


# Add or update a user's reaction to a post
def reactToPost(userID, postID, reaction):
    if not isValidPost(userID, respondID=postID):
        return -1

    mySQLOperation = ("SELECT COUNT(*) FROM Reaction"
                    " WHERE userID = %s AND postID = %s;")
    mySQLParams = [userID, postID]
    if execQuery(mySQLOperation, mySQLParams) != 0:
        return -1

    if cursor.fetchone()[0] > 0:
        mySQLOperation = ("UPDATE Reaction"
                        " SET reaction = %s"
                        " WHERE userID = %s AND postID = %s;")
        mySQLParams = [reaction, userID, postID]
        if execQuery(mySQLOperation, mySQLParams) != 0:
            return -1
    else:
        mySQLOperation = ("INSERT INTO Reaction"
                        " VALUES (%s, %s, %s);")
        mySQLParams = [userID, postID, reaction]
        if execQuery(mySQLOperation, mySQLParams) != 0:
            return -1

    return saveQueries()


# Add new user to User table
def createUser(userID, firstName, lastName, dateOfBirth, religion):
    mySQLOperation = ("INSERT INTO User"
                    " VALUES (%s,  %s, %s, %s, %s);")
    mySQLParams = [userID, firstName, lastName, dateOfBirth, religion]
    if execQuery(mySQLOperation, mySQLParams) != 0:
        return -1
    return saveQueries()


# Add new group to UserGroup table
def createGroup(groupName, members=[]):
    groupID = newGroupID()
    if groupID < 0:
        return -1

    mySQLOperation = ("INSERT INTO UserGroup"
                    " VALUES (%s, %s);")
    mySQLParams = [groupID, groupName]
    if execQuery(mySQLOperation, mySQLParams) != 0:
        return -1

    if len(members) > 0:
        mySQLOperation = "INSERT INTO UserJoins VALUES"
        mySQLParams = []
        for member in members:
            mySQLOperation += " (%s, %s),"
            mySQLParams.append(member)
            mySQLParams.append(groupID)
        mySQLOperation = mySQLOperation[:-1] + ";"
        if execQuery(mySQLOperation, mySQLParams) != 0:
            return -1
    
    return saveQueries()


# Generate new group ID upon new group creation
def newGroupID():
    mySQLOperation = ("SELECT MAX(groupID) FROM UserGroup;")
    if execQuery(mySQLOperation) != 0:
        return -1
    currentMaxGroupID = cursor.fetchone()[0]
    if currentMaxGroupID is None:
        currentMaxGroupID = -1
    return (currentMaxGroupID + 1)


# Add new topic to Topic table, and potential parent topic relations
def createTopic(topicName, parentTopic=None):
    mySQLOperation = ("INSERT INTO Topic"
                    " VALUES (%s);")
    mySQLParams = [topicName]
    if execQuery(mySQLOperation, mySQLParams) != 0:
        return -1

    if parentTopic is not None:
        mySQLOperation = ("INSERT INTO TopicRelation"
                        " VALUES (%s, %s);")
        mySQLParams = [parentTopic, topicName]
        if execQuery(mySQLOperation, mySQLParams) != 0:
            return -1
    
    return saveQueries()
    

# Execute query and check for exceptions; rollback if necessary
def execQuery(operation, params=None):
    try:
        cursor.execute(operation, params)
    except MySqlError as err:
        # if err.errno == errorcode.IntegrityError:
        print('Error: ' + str(err), file=sys.stderr)
        rollbackQueries()
        return -1
    return 0


# Commit queries and check for exceptions
def saveQueries():
    try:
        cnx.commit()
    except MySqlError as err:
        # if err.errno == errorcode.IntegrityError:
        print('Error: ' + str(err), file=sys.stderr)
        return -1
    return 0


# Rollback queries and check for exceptions
def rollbackQueries():
    try:
        cnx.rollback()
    except MySqlError as err:
        # if err.errno == errorcode.IntegrityError:
        print('Error: ' + str(err), file=sys.stderr)
        return -1
    return 0


# Check if user exist in Users entity table
def checkUserExist(userID):
    mySQLOperation = ("SELECT COUNT(*) AS count FROM User"
                    " WHERE userID = %s;")
    mySQLParams = [userID]
    cursor.execute(mySQLOperation, mySQLParams)

    if cursor.fetchone()[0] > 0:
        return True
    return False


# Check if group exist in UserGroup entity table
def checkGroupExist(groupID):
    mySQLOperation = ("SELECT COUNT(*) AS count FROM UserGroup"
                    " WHERE groupID = %s;")
    mySQLParams = [groupID]
    cursor.execute(mySQLOperation, mySQLParams)

    if cursor.fetchone()[0] > 0:
        return True
    return False


# Check if topic exist in Topic entity table
def checkTopicExist(topicName):
    mySQLOperation = ("SELECT COUNT(*) AS count FROM Topic"
                    " WHERE topicName = %s;")
    mySQLParams = [topicName]
    cursor.execute(mySQLOperation, mySQLParams)

    if cursor.fetchone()[0] > 0:
        return True
    return False
