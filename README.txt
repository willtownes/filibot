This is a website for Filipino Botany. The main purpose of the site is to provide easy access for students and researchers interested in the plants of the Philippines to a library of botanical images.

The site is implemented using the following tools:
scripting language: python 2.7
web framework:      web.py
database:           sqlite 3

Basic usage for running the app locally:
>> git clone https://github.com/willtownes/filibot.git
>> cd filibot
>> python setup.py install
At this point, if you have a copy of plants.sqlite (the database), drop it into the subfolder /data/. The schema is stored as /data/dbschema.sql.
>> python bin/app.py
It should show something on the command line like:
http://0.0.0.0:8080/
This means the application is running. Now in a browser you can go to:
http://localhost:8080
and you should see the index html page.
The page may not display completely without the plants.sqlite database in the /data/ subfolder. If you want a copy of the database, contact me.