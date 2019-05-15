-- Q4 Creating tables
Create table EmployeeData (
empID int(11) primary key, 
firstName varchar(100), 
lastName varchar(100), 
job varchar(100), 
salary int(11)
);

Create table EmployeeMiddleName (
empID int(11) primary key, 
middleName varchar(100),
foreign key(empID) references EmployeeData(empID)
);

Create table DepartmentName (
deptID int(11) primary key, 
deptName varchar(100)
);

Create table EmployeeDepartment (
empID int, 
deptID int,
foreign key(empID) references EmployeeData(empID), 
foreign key(deptID) references DepartmentName(deptID)
);

Create table Project (
	projID int(11) primary key,
	Title varchar(100),
	Budget int(11),
Funds int(11)
);

CREATE TABLE Assigned (
	empID int(11),
	projID int(11),
	role varchar(11),
FOREIGN KEY (empID) REFERENCES EmployeeData(empID),
FOREIGN KEY (projID) REFERENCES Project(projID));

CREATE TABLE Address (
streetNumber int(11),
streetName varchar(100),
cityName varchar(100),
province varchar(100),
postalCode char(10),
PRIMARY KEY (streetNumber, streetName, cityname, province));

CREATE TABLE DepartmentAddress (
deptID int(11),
streetNumber int(11),
streetName varchar(100),
cityName varchar(100),
province varchar(100),
FOREIGN KEY (deptID) REFERENCES DepartmentName(deptID),
FOREIGN KEY (streetNumber, streetName, cityName, province) REFERENCES Address(streetNumber, streetName, cityName, province));


-- Q5 Create views that correspond to the tables which miss attributes.
 
CREATE VIEW Employee
AS SELECT EData.empID, CONCAT(EData.firstName, ' ', IFNULL(EMN.middleName, ''), ' ', EData.lastName) AS empName, EData.job, EDept.deptID, EData.salary
FROM EmployeeData AS EData
LEFT OUTER JOIN EmployeeMiddleName AS EMN ON (EData.empID = EMN.empID)
LEFT OUTER JOIN EmployeeDepartment AS EDept ON (EData.empID = EDept.empID);


CREATE VIEW Department
AS SELECT DN.deptID, DN.deptName, CONCAT(DA.streetNumber, ' ', DA.streetName, ', ', DA.cityName, ', ', DA.cityName, ', ', DA.province) as location 
FROM DepartmentName AS DN
LEFT OUTER JOIN DepartmentAddress AS DA ON (DN.deptID = DA.deptID)
INNER JOIN Address AS A ON (DA.streetNumber = A.streetNumber AND DA.streetName = A.streetName AND DA.cityName = A.cityName AND DA.province = A.province);




-- Q6 Stored procedure to increase the salary of employees in Waterloo

DROP PROCEDURE IF EXISTS payRaise;

DELIMITER //

CREATE PROCEDURE payRaise(IN inEmpID int(11), IN inPercentageRaise double(4, 2), OUT errorCode int(11))
BEGIN
	IF inPercentageRaise > 0.10 OR inPercentageRaise < 0 THEN
    	SET errorCode = -1;
	ELSEIF NOT EXISTS(SELECT * FROM EmployeeData WHERE empID = inEmpID) THEN
    	SET errorCode = -2;
	ELSE
    	UPDATE EmployeeData SET salary = ROUND(salary * (1.0 + inPercentageRaise))
    	WHERE empID = inEmpID;
    	SET errorCode = 0;
	END IF;
END//

CREATE PROCEDURE updateWaterlooSalaries()
BEGIN
	DECLARE i INT(11) DEFAULT 0;

	DROP TEMPORARY TABLE IF EXISTS WaterlooEmployees;
	CREATE TEMPORARY TABLE WaterlooEmployees
    	(SELECT DISTINCT(empID)
    	FROM EmployeeData
    	LEFT OUTER JOIN EmployeeDepartment USING (empID)
    	INNER JOIN DepartmentAddress USING (deptID)
    	WHERE cityName='Waterloo');
   	 
	SET i = 0;
	SELECT COUNT(*) INTO @size FROM WaterlooEmployees;
	WHILE i < @size DO
    	SELECT empID INTO @empID FROM WaterlooEmployees LIMIT i,1;
    	CALL payRaise(@empID, 0.05, @out_value);
    	SET i = i + 1;
	END WHILE;

	DROP TEMPORARY TABLE WaterlooEmployees;
END//

DELIMITER ;
