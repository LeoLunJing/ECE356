-- Part 1 
-- 1a
SELECT COUNT(*) FROM Master AS M
WHERE M.`birthDay` = 0 OR M.`birthMonth` = 0 OR M.`birthYear` = 0;

SELECT COUNT(*) FROM Master AS M
WHERE M.`birthDay` = "" OR M.`birthMonth` = "" OR M.`birthYear` = "";

/*
+----------+
| COUNT(*) |
+----------+
|      449 |
+----------+
1 row in set (0.02 sec)
*/


-- 1b
SELECT
(SELECT count(DISTINCT M.playerID) FROM HallOfFame AS H LEFT outer join Master AS M
ON H.playerID = M.playerID 
WHERE M.deathYear = '' AND M.deathMonth = '' AND  M.deathDay = '' AND  M.deathCountry = '' AND  M.deathState = '' AND  M.deathCity = '')
-
(SELECT count(DISTINCT M.playerID) FROM HallOfFame AS H LEFT outer join Master AS M
ON H.playerID = M.playerID 
WHERE M.deathYear <> '' OR  M.deathMonth <> '' OR  M.deathDay <> '' OR  M.deathCountry <> '' OR  M.deathState <> '' OR  M.deathCity <> '') as difference;

/*
+------------+
| difference |
+------------+
|        -47 |
+------------+
1 row in set (0.05 sec)
*/

-- 1c
SELECT M.nameFirst, M.nameGiven, M.nameLast, SUM(S.salary) as SS FROM Salaries AS S LEFT OUTER JOIN Master AS M
USING (playerID)
GROUP BY playerID 
ORDER BY SS DESC
LIMIT 1;
/*
+-----------+--------------------+-----------+-----------+
| nameFirst | nameGiven          | nameLast  | SS        |
+-----------+--------------------+-----------+-----------+
| Alex      | Alexander Enmanuel | Rodriguez | 398416252 |
+-----------+--------------------+-----------+-----------+
1 row in set (0.17 sec)
*/

-- 1d
SELECT
(SELECT SUM(HR) FROM Batting as B)
/
(SELECT COUNT(DISTINCT playerID) FROM Batting)
AS average_HR;
/*
+------------+
| average_HR |
+------------+
|    15.2938 |
+------------+
1 row in set (0.16 sec)
*/


-- 1e
SELECT
(SELECT SUM(HR) FROM Batting as B)
/
(SELECT COUNT(DISTINCT T.playerID) FROM
(SELECT playerID FROM Batting as B
GROUP BY playerID
HAVING Sum(B.HR) > 0) AS T) as average_HR_gt1HR;
/*
+------------------+
| average_HR_gt1HR |
+------------------+
|          37.3944 |
+------------------+
1 row in set (0.37 sec)
*/


-- 1f
SELECT count(*) FROM

(SELECT * FROM
(SELECT playerID, SUM(HR) as sumHR FROM Batting as B 
GROUP BY playerID) as T
WHERE T.sumHR > (
SELECT
(SELECT SUM(HR) FROM Batting as B)
/
(SELECT COUNT(DISTINCT playerID) FROM Batting)
AS average_HR
)) AS T_goodbatter 

INNER join

(SELECT * FROM
(SELECT playerID, SUM(SHO) as sumSHO FROM Pitching as P 
GROUP BY playerID) as T
WHERE T.sumSHO > (
SELECT
(SELECT SUM(SHO) FROM Pitching as P)
/
(SELECT COUNT(DISTINCT playerID) FROM Pitching)
AS average_SHO
)) AS T_goodpitcher

using (playerID);
/*
+----------+
| count(*) |
+----------+
|       39 |
+----------+
1 row in set (0.74 sec)
*/

-- 2
LOAD DATA LOCAL INFILE "~/Downloads/Fielding.csv" INTO TABLE Fielding
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;


-- 3
-- (1)
/*
	2.1 Master Table
		Primary Key: playerID
		
	2.2 Batting Table
		
*/

-- Team : yearID, teamID 
SELECT count(*) FROM Teams;	
SELECT count(*) FROM Teams as T inner join Teams as R 
WHERE T.yearID = R.yearID AND T.teamID = R.teamID;	


-- AwardsSharePlayers: awardID, yearID, playerID
SELECT count(*) FROM AwardsSharePlayers;
SELECT count(A.awardID) FROM AwardsSharePlayers as A inner join AwardsSharePlayers as B 
Where A.awardID = B.awardID AND A.yearID = B.yearID AND A.playerID = B.playerID;

-- AwardsPlayers: awardID, yearID, playerID, lgID
SELECT count(*) FROM AwardsPlayers;
SELECT count(A.awardID) FROM AwardsPlayers as A inner join AwardsPlayers as B 
Where A.awardID = B.awardID AND A.yearID = B.yearID AND A.playerID = B.playerID AND A.lgID = B.lgID;
SELECT * FROM AwardsPlayers as A inner join AwardsPlayers as B 
Where A.awardID = B.awardID AND A.yearID = B.yearID AND A.playerID = B.playerID AND A.lgID <> B.lgID;

-- AwardsShareManagers: awardID, yearID, playerID
SELECT count(*) FROM AwardsShareManagers;
SELECT count(A.awardID) FROM AwardsShareManagers as A inner join AwardsShareManagers as B 
Where A.awardID = B.awardID AND A.yearID = B.yearID AND A.playerID = B.playerID;

-- AwardsManagers: awardID, yearID, playerID
SELECT count(*) FROM AwardsManagers;
SELECT count(A.awardID) FROM AwardsManagers as A inner join AwardsManagers as B 
Where A.awardID = B.awardID AND A.yearID = B.yearID AND A.playerID = B.playerID;


SELECT count(*) FROM AllstarFull;
SELECT count(*) FROM AllstarFull as A inner join AllstarFull as B 
Where A.playerID = B.playerID AND A.yearID = B.yearID AND A.teamID = B.teamID AND A.gameID = B.gameID;

SELECT count(*) FROM Teams;
SELECT count(*) FROM Teams as A inner join Teams as B 
Where A.yearID = B.yearID AND A.teamID = B.teamID;

SET foreign_key_checks = 0;

-- Primary Keys

-- 2.1 Master
ALTER TABLE Master ADD PRIMARY KEY (playerID);

-- 2.8 Teams table
ALTER TABLE Teams 
ADD PRIMARY KEY (yearID, teamID);

-- 2.5 AllstarFull table
ALTER TABLE AllstarFull 
ADD PRIMARY KEY (gameID, playerID, yearID, teamID);

-- 2.11 TeamFranchises table
ALTER TABLE TeamFranchises 
ADD PRIMARY KEY (franchID);

-- 2.16 SeriesPost table
ALTER TABLE ManagersHalf 
ADD PRIMARY KEY (yearID);

-- 2.17 AwardsManagers table
ALTER TABLE AwardsManagers
ADD PRIMARY KEY (awardID, yearID, playerID);

-- 2.18 AwardsPlayers table
ALTER TABLE AwardsPlayers
ADD PRIMARY KEY (awardID, yearID, lgID, playerID);

-- 2.19 AwardsShareManagers table
ALTER TABLE AwardsShareManagers
ADD PRIMARY KEY (awardID, yearID, playerID);

-- 2.20 AwardsSharePlayers table
ALTER TABLE AwardsSharePlayers
ADD PRIMARY KEY (awardID, yearID, playerID);

-- 2.23 Schools table
ALTER TABLE Schools
ADD PRIMARY KEY (schoolID);

-- 2.26 Parks table
ALTER TABLE Parks
ADD PRIMARY KEY (`park.key`);


/* Foreign Keys*/

-- 2.2 Batting Table
ALTER TABLE Batting 
ADD FOREIGN KEY (playerID) REFERENCES Master(playerID), 
ADD FOREIGN KEY (yearID, teamID) REFERENCES Teams(yearID, teamID);


-- 2.3 Pitching table
ALTER TABLE Pitching 
ADD FOREIGN KEY (playerID) REFERENCES Master(playerID),
ADD FOREIGN KEY (yearID, teamID) REFERENCES Teams(yearID, teamID);


-- 2.4 Fielding Table
ALTER TABLE Fielding 
ADD FOREIGN KEY (playerID) REFERENCES Master(playerID),
ADD FOREIGN KEY (yearID, teamID) REFERENCES Teams(yearID, teamID);

-- 2.5 AllstarFull table
ALTER TABLE AllstarFull 
ADD FOREIGN KEY (playerID) REFERENCES Master(playerID),
ADD FOREIGN KEY (yearID, teamID) REFERENCES Teams(yearID, teamID);

-- 2.6  HallOfFame table
ALTER TABLE AllstarFull 
ADD FOREIGN KEY (playerID) REFERENCES Master(playerID),
ADD FOREIGN KEY (yearID) REFERENCES Teams(yearID);

-- 2.7 Managers table
ALTER TABLE Managers 
ADD FOREIGN KEY (playerID) REFERENCES Master(playerID),
ADD FOREIGN KEY (yearID, teamID) REFERENCES Teams(yearID, teamID);

-- 2.9 BattlingPost table
ALTER TABLE Batting 
ADD FOREIGN KEY (playerID) REFERENCES Master(playerID),
ADD FOREIGN KEY (yearID, teamID) REFERENCES Teams(yearID, teamID);

-- 2.10 PitchingPost table
ALTER TABLE Pitching 
ADD FOREIGN KEY (playerID) REFERENCES Master(playerID),
ADD FOREIGN KEY (yearID, teamID) REFERENCES Teams(yearID, teamID); 

-- 2.12 FieldingOF table
ALTER TABLE FieldingOF 
ADD FOREIGN KEY (playerID) REFERENCES Master(playerID),
ADD FOREIGN KEY (yearID) REFERENCES Teams(yearID);

-- 2.13 ManagersHalf table
ALTER TABLE ManagersHalf 
ADD FOREIGN KEY (playerID) REFERENCES Master(playerID),
ADD FOREIGN KEY (yearID, teamID) REFERENCES Teams(yearID, teamID);

-- 2.14 TeamsHalf table
ALTER TABLE ManagersHalf 
ADD FOREIGN KEY (yearID, teamID) REFERENCES Teams(yearID, teamID);

-- 2.15 Salaries table
ALTER TABLE Salaries 
ADD FOREIGN KEY (playerID) REFERENCES Master(playerID),
ADD FOREIGN KEY (yearID, teamID) REFERENCES Teams(yearID, teamID);

-- 2.17 AwardsManagers table
ALTER TABLE AwardsManagers
ADD FOREIGN KEY (playerID) REFERENCES Master(playerID);


-- 2.18 AwardsPlayers table
ALTER TABLE AwardsPlayers
ADD FOREIGN KEY (playerID) REFERENCES Master(playerID);

-- 2.19 AwardsShareManagers table
ALTER TABLE AwardsShareManagers
ADD FOREIGN KEY (playerID) REFERENCES Master(playerID);

-- 2.20 AwardsSharePlayers table
ALTER TABLE AwardsSharePlayers
ADD FOREIGN KEY (playerID) REFERENCES Master(playerID);

-- 2.21 FieldingPost table
ALTER TABLE FieldingPost
ADD FOREIGN KEY (playerID) REFERENCES Master(playerID),
ADD FOREIGN KEY (yearID, teamID) REFERENCES Teams(yearID, teamID);

-- 2.22 Appearances table
ALTER TABLE Appearances
ADD FOREIGN KEY (yearID, teamID) REFERENCES Teams(yearID, teamID),
ADD FOREIGN KEY (playerID) REFERENCES Master(playerID);

-- 2.24 CollegePlaying table
ALTER TABLE CollegePlaying
ADD FOREIGN KEY (playerID) REFERENCES Master(playerID),
ADD FOREIGN KEY (schoolID) REFERENCES Schools(schoolID);

-- 2.25 FieldingOFsplit table
ALTER TABLE FieldingOFsplit
ADD FOREIGN KEY (playerID) REFERENCES Master(playerID),
ADD FOREIGN KEY (yearID, teamID) REFERENCES Teams(yearID, teamID);

-- 2.27 HomeGames table
ALTER TABLE HomeGames
ADD FOREIGN KEY (`park.key`) REFERENCES Parks(`park.key`);


SET foreign_key_checks = 1;

