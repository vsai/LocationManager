LocationManager
===============

Web application using Python (Flask, SQLAlchemy), and HTML, CSS, JavaScript to allow users to manage their favorite locations

Uses backbone.js


Postgresql server:
START: 		pg_ctl -D /usr/local/var/postgres -l /usr/local/var/postgres/server.log start
TERMINATE: 	pg_ctl -D /usr/local/var/postgres stop -s -m fast

Web Server:
To Run: python app.py

Request Handlers:
-------------------------------------------------------
Request		URL					Form Params
-------------------------------------------------------
GET	 		/locations
GET			/locations/:id
POST		/locations			name, address, lng, lat
PUT			/locations/:id		name, address, lng, lat
DELETE		/locations/:id
-------------------------------------------------------

The database must be created beforehand. The table need not be created prior to use.

Database name is specified in: app.py
