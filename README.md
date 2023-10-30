We have built a Flask Application using RESTful API - Error Handling, Authentication.

Team Members:
Devashri Manepatil (885185645)
Apoorva Machale (885209536)

1. Setup Virtual Env using command: virtualenv -p python3 myvenv
3. Activate the virutal env using command: source myvenv/bin/activate
4. Install the packages mentioned in the requirements.txt: pip freeze > requirements.txt
5. In Mysql create database "web_backend_project"
6. Create 2 schemas named users and appointments:
CREATE TABLE IF NOT EXISTS `users` (
`student_id` int NOT NULL AUTO_INCREMENT,
`username` varchar(50) NOT NULL,
`password` varchar(255) NOT NULL,
`email` varchar(100) NOT NULL,
 PRIMARY KEY (`student_id`)
) ENGINE=InnODB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


CREATE TABLE IF NOT EXISTS `student_admissions` (
`student_id` int NOT NULL AUTO_INCREMENT,
`fullName` varchar(50) NOT NULL,
`phoneNumber` varchar(255) NOT NULL,
`email` varchar(100) NOT NULL,
`date` varchar(20) NOT NULL,
`cgpa` varchar(10) NOT NULL,
`area` varchar(20) NOT NULL,
`city` varchar(20) NOT NULL,
`state` varchar(20) NOT NULL,
`postalcode` varchar(20) NOT NULL,
 PRIMARY KEY (`student_id`) 
) ENGINE=InnODB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

7. Make requirements changes in the app.py with the username and password for your database installed on your machine.
8. Change the upload path in app.py based on the PATH you have on your computer to make use of upload API.


