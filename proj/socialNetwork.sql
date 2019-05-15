CREATE DATABASE IF NOT EXISTS SocialNetwork;
USE SocialNetwork;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

drop table if exists User;
drop table if exists Post;
drop table if exists PostTopics;
drop table if exists UserGroup;
drop table if exists Topic;
drop table if exists UserPost;
drop table if exists ReadPost;
drop table if exists Reaction;
drop table if exists TopicRelation;
drop table if exists UserJoins;
drop table if exists UserFollowsTopic;
drop table if exists UserFollowsUser;
drop table if exists GroupPost;
drop table if exists PostResponse;

create table User (
    userID char(10),
    firstName char(10),
    lastName char(10),
    dateOfBirth date,
    religion char(50),
    primary key (userID)
);
insert into User values ('bob001', 'Bob', 'Bombastic', '1997-01-01', 'Hinduism'),
                        ('alex001', 'Alex', 'Anchor', '1949-12-12', 'Atheist'),
                        ('craig001', 'Craig', 'Covera', '1963-05-16', 'Christianity'),
                        ('dave001', 'David', 'Demilo', '1986-04-05', 'Buddhism'),
                        ('eli001', 'Elias', 'Erazor', '2001-07-30', 'Islam');

create table Topic (
    topicName varchar(50),
    primary key (topicName)
);
insert into Topic values    ('uw'),
                            ('sports'),
                            ('baseball'),
                            ('soccer'),
                            ('worldcup'),
                            ('ece356');

create table UserGroup (
    groupID int(4), 
    groupName varchar(50),
    primary key (groupID)
);
insert into UserGroup values (0, 'The Best UserGroup Ever'),
                             (1, 'ECE Study'),
                             (2, 'TestGroup');

create table Post (
    postID int(4),
    timestamp datetime,
    content text(256),
    primary key (postID)
);
insert into Post values (1, '2006-12-31 23:54:13', 'watching sports on tv'),
                        (2, '2008-07-29 05:40:09', 'something about uw ...'),
                        (3, '2015-02-18 11:39:17', 'something about soccer'),
                        (4, '2017-06-15 19:30:07', 'something on sports ...'),
                        (5, '2017-12-25 15:55:55', 'baseball homeruns idk'),
                        (6, '2018-03-25 09:25:34', 'uw greatest school evar'),
                        (7, '2018-08-01 03:03:12', 'database technical jargon'),
                        (8, '2018-09-19 17:10:52', 'worldcup suggestions'),
                        (9, '2018-11-30 07:20:37', 'test group does nothing'),
                        (10, '2019-04-05 03:03:25', 'topicless ramble');

create table PostTopics (
    postID int(4),
    topicName varchar(50),
    primary key (postID, topicName),
    foreign key (postID) references Post (postID) on delete cascade,
    foreign key (topicName) references Topic (topicName)
);
insert into PostTopics values   (1, 'sports'),
                                (2, 'uw'),
                                (3, 'soccer'),
                                (4, 'sports'),
                                (5, 'baseball'),
                                (6, 'uw'),
                                (7, 'ece356'),
                                (8, 'worldcup');

create table UserPost (
    userID char(10), 
    postID int(4), 
    primary key (userID, postID),
    foreign key (userID) references User (userID) on delete cascade,
    foreign key (postID) references Post (postID) on delete cascade
);
insert into UserPost values ('bob001', 1),
                            ('bob001', 2),
                            ('alex001', 3),
                            ('alex001', 4),
                            ('craig001', 5),
                            ('craig001', 6),
                            ('dave001', 7),
                            ('eli001', 8),
                            ('eli001', 9),
                            ('alex001', 10);

create table ReadPost (
    userID char(10), 
    postID int(4),
    primary key (userID, postID),
    foreign key (userID) references User (userID) on delete cascade,
    foreign key (postID) references Post (postID) on delete cascade
);
insert into ReadPost values ('bob001', 3),
                            ('alex001', 1);

create table Reaction (
    userID char(10),
    postID int(4), 
    reaction enum('like', 'dislike', 'funny', 'sad'),
    primary key (userID, postID),
    foreign key (userID) references User (userID) on delete cascade,
    foreign key (postID) references Post (postID) on delete cascade
);
insert into Reaction values  ('bob001', 1, 'like'),
                            ('bob001', 3, 'dislike'),
                            ('alex001', 2, 'funny');

create table TopicRelation (
    parentTopic varchar(50), 
    subTopic varchar(50), 
    primary key (parentTopic, subTopic),
    foreign key (parentTopic) references Topic (topicName),
    foreign key (subTopic) references Topic (topicName) on delete cascade
);
insert into TopicRelation values ('uw', 'ece356'),
                                    ('sports', 'baseball'),
                                    ('sports', 'soccer'),
                                    ('soccer', 'worldcup');

create table UserJoins (
    userID char(10), 
    groupID int(4), 
    primary key (userID, groupID),
    foreign key (userID) references User (userID) on delete cascade,
    foreign key (groupID) references UserGroup (groupID) on delete cascade
); 
insert into UserJoins values    ('bob001', 0),
                                ('bob001', 1),
                                ('bob001', 2),
                                ('alex001', 0),
                                ('eli001', 2),
                                ('craig001', 1),
                                ('dave001', 2),
                                ('eli001', 0),
                                ('alex001', 2);

create table UserFollowsTopic (
    userID char(10), 
    topicName varchar(50), 
    primary key (userID, topicName),
    foreign key (userID) references User (userID) on delete cascade,
    foreign key (topicName) references Topic (topicName)
);
insert into UserFollowsTopic values ('bob001', 'ece356'),
                                    ('bob001', 'sports');

create table UserFollowsUser (
    FollowerUserID char(10), 
    FollowedUserID char(10), 
    primary key (FollowerUserID, FollowedUserID),
    foreign key (FollowerUserID) references User (userID) on delete cascade,
    foreign key (FollowedUserID) references User (userID) on delete cascade
);
insert into UserFollowsUser values ('bob001', 'alex001');

create table GroupPost (
    postID int(4),
    groupID int(4),
    primary key (postID),
    foreign key (postID) references Post (postID) on delete cascade,
    foreign key (groupID) references UserGroup (groupID) on delete cascade
);
insert into GroupPost values    (1, 0),
                                (6, 1),
                                (9, 2);

create table PostResponse (
    responderPostID int(4),
    respondedPostID int(4),
    primary key (responderPostID, respondedPostID),
    foreign key (responderPostID) references Post (postID) on delete cascade,
    -- Cascade delete for testing purposes; would break actual "responding" posts
    foreign key (respondedPostID) references Post (postID) on delete cascade
);
insert into PostResponse values (2, 3),
                                (4, 8),
                                (2, 7);

SET FOREIGN_KEY_CHECKS = 1;

