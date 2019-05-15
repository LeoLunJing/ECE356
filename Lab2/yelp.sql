/*
	YELP 
*/

-- a 
CREATE INDEX user_1 on user (review_count);

SELECT name FROM user 
ORDER BY review_count DESC
LIMIT 1;
/*
+--------+
| name   |
+--------+
| Victor |
+--------+
1 row in set (0.70 sec)
*/

-- b
CREATE INDEX business_1 on business (review_count);

SELECT name FROM business 
ORDER BY review_count DESC
LIMIT 1;
/*
+--------------+
| name         |
+--------------+
| Mon Ami Gabi |
+--------------+
1 row in set (0.13 sec)
*/

-- c
 
-- No index added

SELECT AVG(review_count) FROM user;
/*
+-------------------+
| AVG(review_count) |
+-------------------+
|           24.3193 |
+-------------------+
1 row in set (0.69 sec)
*/


-- d
CREATE INDEX user_2 on user (user_id);
CREATE INDEX review_1 on review (user_id);


SELECT COUNT(*) FROM 
(SELECT user_id, average_stars FROM user) as A inner join 
(SELECT AVG(stars) as avg_stars, user_id FROM review  
GROUP BY user_id ) as B
USING (user_id)
WHERE ABS(A.average_stars - B.avg_stars) > 0.5;
/* 
+----------+
| COUNT(*) |
+----------+
|       66 |
+----------+
1 row in set (13.60 sec) */

-- e 

CREATE INDEX user_3 on user (review_count);

SELECT
(SELECT count(*) FROM user Where review_count > 10)
/
(SELECT count( distinct user_id) FROM user) as fraction;
/* 
+----------+
| fraction |
+----------+
|   0.3311 |
+----------+
1 row in set (1.85 sec) 
*/

-- f
CREATE INDEX user_4 on user (review_count, user_id);


SELECT AVG(LENGTH(text)) FROM user as U inner join review as R
USING (user_id)
WHERE U.review_count > 10;
/*
+-------------------+
| AVG(LENGTH(text)) |
+-------------------+
|          698.7808 |
+-------------------+
1 row in set (42.83 sec)
*/
