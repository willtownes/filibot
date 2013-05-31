This is a website for Filipino Botany. The main purpose of the site is to provide easy access for students and researchers interested in the plants of the Philippines to a library of botanical images.

The site is implemented using the following tools:
scripting language: python 2.7
web framework:      web.py
database:           sqlite 3

Basic usage for running the app locally:
After cloning (or installing via package manager), make sure required libraries are installed (see above). Then cd to the folder filibot and run:
python bin/app.py
It should show something on the command line like:
http://0.0.0.0:8080/
This means the application is running. Now in a browser you can go to:
http://localhost:8080
and you should see the index html page.
The page may not display properly without the plants.sqlite database in the /data/ subfolder. If you want a copy of the database, contact me.

