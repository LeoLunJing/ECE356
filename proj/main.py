import dbConnection
import query
import re
import argparse

def main():
    parser = argparse.ArgumentParser(description='Social network client (ECE356 Project)')
    parser.add_argument('-U', '--sqlUser', metavar='sqlu', default=None,
                        help='Local mySQL user.')
    parser.add_argument('-P', '--sqlPass', metavar='sqlp', default=None,
                        help='Local mySQL password.')
    parser.add_argument('-u', '--userID', metavar='uID', default=None,
                        help='User ID of the client user.')
    parser.add_argument('-g', '--groupID', metavar='gID', default=None,
                        help='Group ID.')
    parser.add_argument('-G', '--groupName', metavar='gName', default=None,
                        help='Group name.')
    parser.add_argument('-m', '--members', metavar='mem', default=[], nargs='+',
                        help='Members to add to a newly created group.')
    parser.add_argument('-t', '--topics', metavar='topicList', default=[], nargs='+',
                        help='Topics (multiple allowed).')
    parser.add_argument('-T', '--parentTopic', metavar='parentTopic', default=None,
                        help='Parent topic of a topic to create.')
    parser.add_argument('-c', '--content', metavar='c', default=None,
                        help='Content (of a post).')
    parser.add_argument('-f', '--followID', metavar='fID', default=None,
                        help='User ID to follow.')
    parser.add_argument('-p', '--postID', metavar='pID', default=None,
                        help='Post ID to respond/react to.')
    parser.add_argument('-r', '--reaction', metavar='react', default=None,
                        help='Reaction (of a post).')
    parser.add_argument('-n', '--firstName', metavar='fName', default=None,
                        help='First name of the user.')
    parser.add_argument('-l', '--lastName', metavar='lName', default=None,
                        help='Last name of the user.')
    parser.add_argument('-d', '--dateOfBirth', metavar='DoB', default=None,
                        help='Date of birth of the user.')
    parser.add_argument('-R', '--religion', metavar='relig', default=None,
                        help='Religion of the user.')
    parser.add_argument('-a', '--all', action="store_true",
                        help='Show read and unread posts (most recent 100).')
    parser.add_argument('-s', '--source', metavar='type', default=['user', 'group', 'topic'], nargs='+',
                        help="Check posts from certain source. Sources include: 'user', 'group', 'topic'.")

    parser.add_argument('command', metavar='C',
                        help=('Client command. List of possible commands:\n'
                                'insertPost: Create new post, \n'
								'joinGroup: Join a group, \n'
								'followTopics: Follow a topic, \n'
								'followUser: Follow a user, \n'
								'checkPosts: Check posts, \n'
								'reactToPost: React to a post, \n'
								'createUser: Create a user, \n'
								'createGroup: Create a group, \n'
								'createTopic: Create a topic, \n'
								'leaveGroup: Leave a group, \n'
								'unfollowTopics: Unfollow a topic, \n'
								'unfollowUser: Unfollow a user\n'))
    args = parser.parse_args()
    # print(args)
    # print('\n')
    print('')

    cnx = None
    if args.sqlUser is None or args.sqlPass is None:
        cnx = dbConnection.connectDB()
    else:
        cnx = dbConnection.connectDB(args.sqlUser, args.sqlPass)
    query.setCnxCursor(cnx)

    commandSwitch = {
        'insertPost'    : insertPostCommand,
        'joinGroup'     : joinGroupCommand,
		'followTopics'	: followTopicsCommand,
		'followUser'	: followUserCommand,
		'checkPosts'	: checkPostsCommand,
		'reactToPost'	: reactToPostCommand,
		'createUser'	: createUserCommand,
		'createGroup'	: createGroupCommand,
		'createTopic'	: createTopicCommand,
        'leaveGroup'    : leaveGroupCommand,
        'unfollowTopics' : unfollowTopicsCommand,
        'unfollowUser' : unfollowUserCommand
    }

    if args.command not in commandSwitch:
        print('Unknown command')
        exit()

    commandFcn = commandSwitch[args.command]
    rc = commandFcn(args)    

    if rc == 0:
        print("Command successful")
    else:
        print("Command failed")

    cnx.close()

    # print(query.cnx)
    # print(query.cursor)

    # q1()
    # print("User \"alex001\" exists: " + str(query.checkUserExist("alex001")))
    # print("User \"bob001\" exists: " + str(query.checkUserExist("bob001")))
    # print("User \"craig001\" exists: " + str(query.checkUserExist("craig001")))
    # print("Group 0 exists: " + str(query.checkGroupExist(0)))
    # print("Group 99 exists: " + str(query.checkGroupExist(99)))
    # print("Topic \"ece356\" exists: " + str(query.checkTopicExist("ece356")))
    # print("Topic \"Worst\" exists: " + str(query.checkTopicExist("Worst")))

    # rc = query.createUser("dave001", "David", "Di'Giorno", "1979-04-05", "Atheism")
    # print("Creating new user: " + str(rc))
    # print("User \"dave001\" exists: " + str(query.checkUserExist("dave001")))
    # rc = query.createGroup("Sensational")
    # print("Creating new group: " + str(rc))
    # rc = query.createGroup("SimplySavoury", ["alex001", "bob001"])
    # print("Creating second group: " + str(rc))
    # rc = query.createTopic("universities")
    # print("Creating new topic: " + str(rc))
    # rc = query.createTopic("canadian_universities", "universities")
    # print("Creating second topic: " + str(rc))
    # q2()

    # rc = query.reactToPost("bob001", 2, "like")
    # print("Creating reaction: " + str(rc))
    # query.reactToPost("bob001", 3, "sad")
    # print("Updating reaction: " + str(rc))


def insertPostCommand(args):
    if args.userID is None or (args.content is None and args.file is None):
        print('insertPost command has not received require arguments')
        return -1
    groupID = args.groupID
    if groupID is not None:
        groupID = int(groupID)
    respondID = args.postID
    if respondID is not None:
        respondID = int(respondID)
    return query.insert_post(args.userID, args.content, args.topics, groupID, respondID);


def joinGroupCommand(args):
    if args.userID is None or args.groupID is None:
        print('joinGroup command has not received required arguments')
        return -1
    groupID = int(args.groupID)
    return query.joinGroup(args.userID, groupID)


def followTopicsCommand(args):
    if args.userID is None or len(args.topics) == 0:
        print('followTopics command has not received required arguments')
        return -1
    return query.followTopics(args.userID, args.topics)


def followUserCommand(args):
    if args.userID is None or args.followID is None:
        print('followUser command has not received required arguments')
        return -1
    return query.followUser(args.userID, args.followID)


def checkPostsCommand(args):
    if args.userID is None:
        print('checkPosts command has not received required arguments')
        return -1
    return query.checkPosts(args.userID, args.all, args.source)


def reactToPostCommand(args):
    if args.userID is None or args.postID is None or args.reaction is None:
        print('reactToPost command has not received required arguments')
        return -1
    postID = int(args.postID)
    return query.reactToPost(args.userID, postID, args.reaction)


def createUserCommand(args):
    if args.userID is None or args.firstName is None or args.lastName is None or args.dateOfBirth is None or args.religion is None:
        print('createUser command has not received required arguments')
        return -1
    return query.createUser(args.userID, args.firstName, args.lastName, args.dateOfBirth, args.religion)


def createGroupCommand(args):
    if args.groupName is None:
        print('createGroup command has not received required arguments')
        return -1
    return query.createGroup(args.groupName, args.members)


def createTopicCommand(args):
    if len(args.topics) == 0:
        print('createTopic command has not received required arguments')
        return -1
    elif len(args.topics) != 1:
        print('createTopic command can only create one topic at a time')
        return -1
    return query.createTopic(args.topics[0], args.parentTopic)


def leaveGroupCommand(args):
    if args.userID is None or args.groupID is None:
        print('leaveGroup command has not received required arguments')
        return -1
    groupID = int(args.groupID)
    return query.leaveGroup(args.userID, groupID)

def unfollowTopicsCommand(args):
    if args.userID is None or len(args.topics) == 0:
        print('unfollowTopics command has not received required arguments')
        return -1
    return query.unfollowTopics(args.userID, args.topics)

def unfollowUserCommand(args):
    if args.userID is None or args.followID is None:
        print('unfollowUser command has not received required arguments')
        return -1
    return query.unfollowUser(args.userID, args.followID)

def q1():
    # myuser = User("bob001")
    # myuser.post("Hi", topics=['ece356', 'uw'])
    query.insert_post("bob001", "asdf", topics=['ece356', 'uw'], groupID=1, responsePostID=3)


def q2():
    myuser = User("bob001")
#  -U bob -P -C "hellow world!"
#  -

if __name__ == '__main__':
    main()
