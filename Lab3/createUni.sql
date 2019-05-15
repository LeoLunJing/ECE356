-- Lab 3
drop table if exists Offering;
drop table if exists Instructor;
drop table if exists Prereq;
drop table if exists Course;
drop table if exists Classroom;
drop table if exists Department;

create table Classroom (roomID char(8), Building char(4), Room decimal(4), Capacity int, primary key (roomID));
insert into Classroom values ('E74417', 'E7', 4417, 138),
       	    	      	     ('E74053', 'E7', 4053 , 144 ),
			     ('RCH111' , 'RCH' , 111 , 91 ),
			     ('RCH101' , 'RCH', 101 , 250 );


create table Department (deptID char(8), deptName varchar(50), faculty varchar(50), primary key(deptID));
insert into Department values ('ECE' , 'Electrical and Computer Engineering' , 'Engineering' ),
       	    	       	      ('CS'  , 'Computer Science' , 'Math' ),
			      ('MATH'  , 'Math' , 'Math' ),
			      ('C&O'  , 'Combinatorics and Optimization' , 'Math' );

create table Instructor(instID int, instName char(10), deptID char(4), sessional bool, primary key (instID), foreign key (deptID) references Department(deptID));
insert into Instructor values (1 , 'Nelson' , 'ECE' , false ),
       	    	       	      (3 , 'Jimbo'  , 'ECE' , false   ),
			      (4 , 'Moe'    , 'CS'  , true ),
			      (5 , 'Lenny'  , 'CS'  , false   ),
			      (7 , 'Whoever'  , 'MATH'  , false   );

create table Course (courseID char(8), courseName varchar(50), deptID char(4),
       	     	    primary key(courseID),
       	     	    foreign key (deptID) references Department(deptID));
insert into Course values ('ECE222'  , 'Digital Computers' , 'ECE' ),                -- These three exist so that the foreign key doesn't fail
       	    	   	  ('ECE250'  , 'Algorithms and Data Structures' , 'ECE' ),
       	    	   	  ('ECE290'  , 'Engineering Profession, Ethics, and Law' , 'ECE' ),
       	    	   	  ('ECE356'  , 'Database Systems' , 'ECE' ),
       	    	   	  ('ECE358'  , 'Computer Networks' , 'ECE' ),
			  ('ECE390'  , 'Engineering Design' , 'ECE' ),
			  ('MATH117' , 'Calculus 1'  , 'MATH' );

create table Prereq (courseID char(8), prereqID char(8),
       	     	    primary key(courseID, prereqID),
       	     	    foreign key (courseID) references Course(courseID),
		    foreign key (prereqID) references Course(courseID));
insert into Prereq values ('ECE356'  , 'ECE250'),
       	    	   	  ('ECE358'  , 'ECE222'),
			  ('ECE390'  , 'ECE290' );

create table Offering (courseID char(8), section int, termCode decimal(4), roomID char(8), instID int, enrollment int,
       	     	      primary key(courseID,section,termCode),
       	     	      foreign key (instID) references Instructor(instID),
       	     	      foreign key (roomID) references Classroom(roomID),
		      foreign key (courseID) references Course (courseID));
insert into Offering values ('ECE356'  , 1 , 1191 , 'E74417' , 1 , 64 ),
       	    	     	    ('ECE356'  , 2 , 1191 , 'E74417' , 3 , 123 ),
			    ('ECE290'  , 1 , 1191 , 'E74053' , 3 , 102 ),
			    ('ECE390'  , 1 , 1191 , 'E74053' , 3 , 102 ),
			    ('MATH117' , 1 , 1189 , 'RCH111' , 5 , 89 );

