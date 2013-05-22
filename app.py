from flask import Flask, url_for, request, g
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import *

engine = create_engine('postgresql://vishalsaidaswani@localhost/myfirstdb')
Base.metadata.create_all(engine)
Session = sessionmaker(bind = engine)
app = Flask(__name__)

@app.before_request
def before_request():
	print "Before Request"
	# if (request.endpoint == 'create'):
	g.session = Session()

@app.after_request
def after_request(response):
	print "After request"
	g.session.commit()
	return response

@app.teardown_request
def teardown_request(exception):
	print "Teardown Request"
	g.session.close()

@app.route('/')
def hello_world():
	return 'Hello World!'

@app.route('/create', methods=['GET', 'POST'])
def createLocation():
	print "CREATING"
	if request.method == 'POST':
		print 'Post request for create location'
		lname = request.form['name']
		laddress = request.form['address']
		llat = request.form['lat']
		llng = request.form['lng']
	else:
		lname = 'Work'
		laddress = '405 Howard Street, San Francisco, CA'
		llat = 'def1'
		llng = 'def2'
	
	new_loc = Location(name = lname, address = laddress, lat = llat, lng = llng)
	g.session.add(new_loc)
	return 'Created'

@app.route('/read')
def readLocation():
	pass
	

if __name__ == '__main__':
	app.run(debug=True)