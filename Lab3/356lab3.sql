
DROP PROCEDURE IF EXISTS switchSection;

DELIMITER //

CREATE PROCEDURE switchSection(
  IN courseID char(8), 
  IN section1 int(11),
  IN section2 int(11),
  IN termCode decimal(4,0),
  IN quantity int(11),
  OUT errorCode int(11))
BEGIN
  START TRANSACTION;
	SET errorCode = 0;
	IF
       NOT EXISTS (SELECT * FROM Offering WHERE Offering.courseID = courseID AND Offering.section = section1 AND Offering.termCode = termCode )
       OR
       NOT EXISTS (SELECT * FROM Offering WHERE Offering.courseID = courseID AND Offering.section = section2 AND Offering.termCode = termCode )
       OR
       quantity <= 0;
       OR
       section1 = section2:
       THEN
       		SET errorCode = -1;
	
	ELSE
		SET @enrolled := 0;

		UPDATE Offering
			SET enrollment = (@enrolled := enrollment - quantity)
			WHERE Offering.courseID = courseID AND section = section1 AND Offering.termCode = termCode;

		IF @enrolled < 0 THEN
			SET errorCode = -2;

		ELSE
			SET @limit := 0;
			SELECT @limit := C.Capacity
	        	FROM Offering AS O LEFT OUTER JOIN Classroom AS C USING (roomID)
				WHERE O.courseID = courseID AND O.section = section2 AND O.termCode = termCode
				LIMIT 1;
			UPDATE Offering
				SET enrollment = (@enrolled := enrollment + quantity)
					WHERE Offering.courseID = courseID AND section = section2 AND Offering.termCode = termCode;

			IF @enrolled > @limit THEN
				SET errorCode = -3;
    END IF;     
	
    
                    
    IF errorCode = 0 THEN
       COMMIT;
    ELSE
       ROLLBACK;
    END IF;    
END//


DELIMITER ;


-- Part 3

ALTER TABLE Master ADD PRIMARY KEY (playerID);

ALTER TABLE Teams ADD PRIMARY KEY (yearID, teamID);

ALTER TABLE Batting 
ADD PRIMARY KEY (playerID, yearID, teamID);

ALTER TABLE Batting 
ADD FOREIGN KEY (playerID) REFERENCES Master(playerID);

CREATE INDEX Batting_RBI on Batting (RBI);
CREATE INDEX Batting_HR on Batting (HR);
