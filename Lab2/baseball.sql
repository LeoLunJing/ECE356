-- Part 1 
-- 1a
CREATE INDEX Master_1 on Master (birthDay);
CREATE INDEX Master_2 on Master (birthMonth);
CREATE INDEX Master_3 on Master (birthYear);


EXPLAIN SELECT COUNT(*) FROM Master AS M
WHERE M.`birthDay` = 0 OR M.`birthMonth` = 0 OR M.`birthYear` = 0;

SELECT COUNT(*) FROM Master AS M
WHERE M.`birthDay` = "" OR M.`birthMonth` = "" OR M.`birthYear` = "";



-- DROP INDEX Master_1 on Master;
-- DROP INDEX Master_2 on Master;
-- DROP INDEX Master_3 on Master;

/*
+----------+
| COUNT(*) |
+----------+
|      449 |
+----------+
1 row in set (0.02 sec)
*/


-- 1b
CREATE INDEX Master_1 on Master (birthDay);
CREATE INDEX Master_2 on Master (birthMonth);
CREATE INDEX Master_3 on Master (birthYear);
CREATE INDEX Master_4 on Master (playerID);

EXPLAIN SELECT
(SELECT count(DISTINCT M.playerID) FROM HallOfFame AS H LEFT outer join Master AS M
ON H.playerID = M.playerID 
WHERE M.deathYear = '' AND M.deathMonth = '' AND  M.deathDay = '' AND  M.deathCountry = '' AND  M.deathState = '' AND  M.deathCity = '')
-
(SELECT count(DISTINCT M.playerID) FROM HallOfFame AS H LEFT outer join Master AS M
ON H.playerID = M.playerID 
WHERE M.deathYear <> '' OR  M.deathMonth <> '' OR  M.deathDay <> '' OR  M.deathCountry <> '' OR  M.deathState <> '' OR  M.deathCity <> '') as difference;



-- DROP INDEX Master_1 on Master;
-- DROP INDEX Master_2 on Master;
-- DROP INDEX Master_3 on Master;
-- DROP INDEX Master_4 on Master;

/*
+------------+
| difference |
+------------+
|        -47 |
+------------+
1 row in set (0.05 sec)
*/

-- 1c
CREATE INDEX Salaries_1 on Salaries (playerID);

EXPLAIN SELECT M.nameFirst, M.nameGiven, M.nameLast, SUM(S.salary) as SS FROM Salaries AS S LEFT OUTER JOIN Master AS M
USING (playerID)
GROUP BY playerID 
ORDER BY SS DESC
LIMIT 1;


-- DROP INDEX Salaries_1 on Salaries;

/*
+-----------+--------------------+-----------+-----------+
| nameFirst | nameGiven          | nameLast  | SS        |
+-----------+--------------------+-----------+-----------+
| Alex      | Alexander Enmanuel | Rodriguez | 398416252 |
+-----------+--------------------+-----------+-----------+
1 row in set (0.17 sec)
*/

-- 1d

CREATE INDEX Batting_1 on Batting (playerID);

EXPLAIN
SELECT
(SELECT SUM(HR) FROM Batting as B)
/
(SELECT COUNT(DISTINCT playerID) FROM Batting)
AS average_HR;

-- DROP INDEX Batting_1 on Batting;

/*
+------------+
| average_HR |
+------------+
|    15.2938 |
+------------+
1 row in set (0.16 sec)
*/


-- 1e
/* ALTER TABLE Batting 
DROP FOREIGN KEY playerID;

ALTER TABLE Batting 
ADD FOREIGN KEY (playerID) REFERENCES Master(playerID); */

CREATE INDEX Batting_1 on Batting (playerID);
CREATE INDEX Batting_2 on Batting (HR);
CREATE INDEX Batting_3 on Batting (playerID, HR);


-- DROP INDEX Batting_1 on Batting;
-- DROP INDEX Batting_2 on Batting;
-- DROP INDEX Batting_3 on Batting;

EXPLAIN
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

CREATE INDEX Batting_1 on Batting (playerID, HR);
CREATE INDEX Batting_2 on Batting (HR);
CREATE INDEX Pitching_1 on Pitching (playerID, SHO);
CREATE INDEX Pitching_2 on Pitching (SHO);

EXPLAIN
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



-- DROP INDEX Batting_1 on Batting;
-- DROP INDEX Batting_2 on Batting;
-- DROP INDEX Pitching_1 on Pitching;
-- DROP INDEX Pitching_2 on Pitchin;
