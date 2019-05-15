import unittest
import datetime
import time
import argparse
import sys

import dbConnection
import query

global cnx
global cursor
global sqlUser
global sqlPassword

global testContent
global testUserID1
global testUserID2
global testPostID
global testGroupID
global testTopic1
global testTopic2

testContent = (r'Lorem ipsum dolor sit amet')
                # r', consectetur adipiscing elit,'
                # r' sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. '
                # r'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi '
                # r'ut aliquip ex ea commodo consequat. Duis aute irure dolor in '
                # r'reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla '
                # r'pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa '
                # r'qui officia deserunt mollit anim id est laborum.')
testUserID1 = 'alphatest0'
testUserID2 = 'betatest01'
# TODO: get proper post/group ID
testPostID = 99999999
testGroupID = 99999999
testTopic1 = 'Unit Test Topic Alpha (not actual topic)'
testTopic2 = 'Unit Test Topic Beta (not actual topic)'

class TestInsertPost(unittest.TestCase):

    def testBasic(self):
        self.assertEqual(query.insert_post(testUserID1, testContent), 0)

    def testTopics(self):
        self.assertEqual(query.insert_post(testUserID1, testContent, [testTopic1, testTopic2]), 0)
        self.assertEqual(query.insert_post(testUserID1, testContent, [testTopic1]), testGroupID, 0)
        self.assertEqual(query.insert_post(testUserID1, testContent, [testTopic2], responsePostID=testPostID), 0)

    def testResponses(self):
        self.assertEqual(query.insert_post(testUserID1, testContent, responsePostID=testPostID), 0)
        self.assertEqual(query.insert_post(testUserID1, testContent, [testTopic1], responsePostID=testPostID), 0)
        # TODO: include gorrect groupID and responseID?
        # self.assertEqual(query.insert_post(testUserID1, testContent, groupID=testGroupID, responsePostID=responseID), 0)
        # self.assertEqual(query.insert_post(testUserID1, testContent, [testTopic1], groupID=testGroupID, responsePostID=responseID), 0)

    def testFailure(self):
        badUser = 'zxcvd35yf'
        badGroupID = 999999
        badTopic = 'thisshouldnotbeanactualtopichere~'

        self.assertEqual(query.insert_post(badUser, testContent), -1)
        self.assertEqual(query.insert_post(testUserID1, testContent, [badTopic]), -1)
        self.assertEqual(query.insert_post(testUserID1, testContent, [testTopic1, testTopic2, badTopic]), -1)
        self.assertEqual(query.insert_post(testUserID1, testContent, groupID=badGroupID), -1)
        self.assertEqual(query.insert_post(badUser, testContent, badGroupID, [badTopic]), -1)
        # TODO: include mismatching groupID and responseID?


def insertTestEntities():
    global testPostID

    operation = 'INSERT INTO User VALUES (%s, %s, %s, %s, %s);'
    params = [testUserID1, 'Unit', 'Test', '1999-12-31', 'Robotism']
    cursor.execute(operation, params)

    operation = 'INSERT INTO Topic (topicName) VALUES (%s), (%s);'
    params = [testTopic1, testTopic2]
    cursor.execute(operation, params)

    # TODO: insert group
    # query.insertGroup()

    query.insert_post(testUserID1, testContent, topics=[testTopic1, testTopic2])
    # TODO: insert post with valid group ID

    operation = ("SELECT MAX(postID) FROM Post;")
    cursor.execute(operation)
    testPostID = cursor.fetchone()[0]


def deleteTestEntities():

    operation = 'DELETE FROM User WHERE userID = %s;'
    params = [testUserID1]
    cursor.execute(operation, params)

    operation = 'DELETE FROM User WHERE userID = %s;'
    params = [testUserID2]
    cursor.execute(operation, params)

    operation = 'DELETE FROM Post WHERE postID >= %s;'
    params = [testPostID]
    cursor.execute(operation, params)

    operation = 'DELETE FROM Topic WHERE topicName = %s;'
    params = [testTopic1]
    cursor.execute(operation, params)

    operation = 'DELETE FROM Topic WHERE topicName = %s;'
    params = [testTopic2]
    cursor.execute(operation, params)

    # operation = 'DELETE FROM UserGroup WHERE groupID >= %s;'
    # params = [testGroupID]
    # cursor.execute(operation, params)

    cnx.commit()


def setUpModule():
    global cnx
    global cursor
    global sqlUser
    global sqlPassword
    if sqlUser == None or sqlPassword == None:
        cnx = dbConnection.connectDB()
    else:
        cnx = dbConnection.connectDB(sqlUser, sqlPassword)
    cursor = cnx.cursor()
    query.setCnxCursor(cnx)

    # Remove if currently exists
    deleteTestEntities()
    cnx.commit()
    insertTestEntities()


def tearDownModule():
    global cnx
    deleteTestEntities()
    cnx.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user', metavar='n', default=None,
                        help='mySQL User')
    parser.add_argument('-p', '--password', metavar='p', default=None,
                        help='mySQL Password')
    parser.add_argument('unittest_args', nargs='*')

    args = parser.parse_args()

    sqlUser = args.user
    sqlPassword = args.password    
    unit_argv = sys.argv[:1] + args.unittest_args
    
    unittest.main(argv=unit_argv)
