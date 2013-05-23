from flask import Flask, url_for, request, g#, jsonify
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import *

engine = create_engine('postgresql://vishalsaidaswani@localhost/myfirstdb')
Base.metadata.create_all(engine)
Session = sessionmaker(bind = engine)
app = Flask(__name__)

# app.logger.setLevel('DEBUG')
app.logger.setLevel('INFO')
# app.logger.setLevel('WARNING')

@app.before_request
def before_request():
	app.logger.debug("Before Request")
	# if (request.endpoint == 'create'):
	g.session = Session()

@app.after_request
def after_request(response):
	app.logger.debug("After Request")
	g.session.commit()
	return response

@app.teardown_request
def teardown_request(exception):
	app.logger.debug("Teardown Request")
	if (exception != None):
		app.logger.error("fail - Thrown exception")
	g.session.close()

@app.route('/')
def hello_world():
	return 'Hello World!'

@app.route('/locations', methods=['POST'])
def createLocation():
	app.logger.debug("In createLocation - POST request")
	lname = request.form['name']
	laddress = request.form['address']
	llat = request.form['lat']
	llng = request.form['lng']

	new_loc = Location(name = lname, address = laddress, lat = llat, lng = llng)
	g.session.add(new_loc)
	g.session.flush()
	assert(new_loc.id >= 1)
	app.logger.info("Created new location - id: " + str(new_loc.id))
	return new_loc.id

@app.route('/locations', methods=['GET'])
@app.route('/locations/<int:location_id>', methods=['GET'])
def readLocation(location_id=None):
	app.logger.debug("In readLocation - GET request")
	if (location_id == None):
		# get all 
		read_loc = g.session.query(Location).all()
	else:
		# get specific location_id
		read_loc = g.session.query(Location).get(location_id)
		read_loc = [read_loc]
	print read_loc
	app.logger.info("Got existing location(s)")
	return str(read_loc)

@app.route('/locations/<int:location_id>', methods=['PUT'])
def updateLocation(location_id=None):
	app.logger.debug("In updateLocation - PUT request")
	if (location_id == None):
		app.logger.error("No location_id provided in update request")
		return "fail"
	loc_obj = g.session.query(Location).get(location_id)
	
	app.logger.info("Updated existing location - id: " + str(location_id))
	return "success"

@app.route('/locationsx/<int:location_id>', methods=['GET'])
def deleteLocation(location_id=None):
	if (location_id == None):
		app.logger.error("No location_id provided in delete request")
		return "fail"
	g.session.query(Location).get(location_id).delete()
	app.logger.info("Deleted existing location - id: " + str(location_id))
	return "success"

if __name__ == '__main__':
	app.run(debug=True)