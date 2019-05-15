CREATE INDEX Master_ID ON MASTER(playerID);
CREATE INDEX Batting_ID ON Batting (playerID);
CREATE INDEX Pitching_ID ON Pitching (playerID);
CREATE INDEX HallOfFame_ID ON HallOfFame (playerID);
CREATE INDEX AllstarFull_ID ON AllstarFull (playerID);


SELECT 
M.playerID,  
SUM(B.G),  
SUM(B.AB), 
SUM(B.R), 
Sum(B.H), 
Sum(B.2B), 
Sum(B.3B), 
Sum(B.HR), 
-- Sum(B.RBI), 
Sum(B.SB), 
Sum(B.CS), 
Sum(B.BB), 
Sum(B.SO), 
Sum(B.IBB), 
Sum(B.HBP), 
Sum(B.SH), 
Sum(B.SF), 
Sum(B.GIDP),
Sum(P.W), 
Sum(P.L), 
-- Sum(P.G), 
Sum(P.SHO), 
Sum(P.SV), 
-- Sum(P.IPouts), 
-- Sum(P.H), 
Sum(P.ER), 
-- Sum(P.HR), 
Sum(P.BB), 
Sum(P.SO), 
AVG(P.BAOpp), 
AVG(P.ERA), 
-- Sum(P.IBB), 
-- Sum(P.WP), 
Sum(P.HBP), 
-- Sum(P.BK), 
Sum(P.BFP), 
Sum(P.GF), 
-- Sum(P.R), 
Sum(P.SH),
Sum(P.SF), 
Sum(P.GIDP),
Sum(A.gameNum),
if(H.inducted = 'Y', 'Elected', 'Nominated') as classification

FROM HallOfFame AS H 
INNER JOIN Master AS M ON H.playerID = M.playerID
LEFT JOIN Batting AS B ON (H.playerID = B.playerID)
LEFT JOIN Pitching AS P ON (H.playerID = P.playerID)
LEFT JOIN AllstarFull AS A ON (H.playerID = A.playerID)
where H.category = 'Player'
GROUP BY H.playerID;
