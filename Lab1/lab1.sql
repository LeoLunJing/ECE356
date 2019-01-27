-- Part 1 
-- 1a
SELECT COUNT(*) FROM Master AS M
WHERE M.`birthDay` = 0 OR M.`birthMonth` = 0 OR M.`birthYear` = 0;

SELECT COUNT(*) FROM Master AS M
WHERE M.`birthDay` = "" OR M.`birthMonth` = "" OR M.`birthYear` = "";

-- 1b
SELECT
(SELECT count(DISTINCT M.playerID) FROM HallOfFame AS H LEFT outer join Master AS M
ON H.playerID = M.playerID 
WHERE M.deathYear = '' AND M.deathMonth = '' AND  M.deathDay = '' AND  M.deathCountry = '' AND  M.deathState = '' AND  M.deathCity = '')
-
(SELECT count(DISTINCT M.playerID) FROM HallOfFame AS H LEFT outer join Master AS M
ON H.playerID = M.playerID 
WHERE M.deathYear <> '' OR  M.deathMonth <> '' OR  M.deathDay <> '' OR  M.deathCountry <> '' OR  M.deathState <> '' OR  M.deathCity <> '');


-- 1c
SELECT M.nameFirst, M.nameGiven, M.nameLast, SUM(S.salary) as SS FROM Salaries AS S LEFT OUTER JOIN Master AS M
USING (playerID)
GROUP BY playerID 
ORDER BY SS DESC
LIMIT 1;

-- 1d
SELECT
(SELECT SUM(HR) FROM Batting as B)
/
(SELECT COUNT(DISTINCT playerID) FROM Batting)
AS average_HR;

-- 1e
SELECT
(SELECT SUM(HR) FROM Batting as B)
/
(SELECT COUNT(DISTINCT T.playerID) FROM
(SELECT playerID FROM Batting as B
GROUP BY playerID
HAVING Sum(B.HR) > 0) AS T) as average_HR_gt1HR;

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