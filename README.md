This is my artifact for Secure Software Development module for my masters degree. Over the last 8 weeks (and counting), i have learnt the basics of python(+librarys) , HTML and
CSS. This module has really pushed me to learn something completly different and has been very hard . However through the use of Youtube tutorials, python manuals, Reddit and my fellow students
(esspessially harry) i have made my own webapp with multiple databases. 

One database is in SQLite and the other in MongoDB . I have had some issues allong the way as i orignally written SQLAlchemy which i found later was incorrect. Additioanlly after this issue i then
created one database in SQLite with two tables , one containing the pateint health infomation and the other with login credentials. This was then connected with another file which allowed my to 
use one variable to recall from both tables. However i was later infromed that to acheive a better result, i would have to implement two databases. One in SQ language the other in non-SQ language.
From my lectures and lecturer, he taught us to use mongodb. From alot of my own research i found a tutorial on how to create a mongodb database (local) through mongos community. This helped me alot 
in understanding how mongo worked and how i could implement this into my work. I then created another python file which created the mongo database. For existing users with no username. i created 
a word list which added two words together randomly to create their new username. Their password is a randomly generated and is also hashed. Through harrys (my freind) help i was able to connect the
two databases by using the patient_id as the main link between them. Usersdata now had one unique id whiched caused less confussion. I then make my website look smarter and more professional. From 
tutorials and exsisting stlyesheets, i created my own style sheet which made the website look 'professional'. I had to create a changing navbar for loged in users to see thier account infomation 
and give them the option to update this. i then added code info both my app and html which would query the database and show relvant infomtion to the user, depedning on their session id which 
is set to be the same as their p_id and u_id. 
