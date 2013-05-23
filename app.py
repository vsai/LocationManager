from flask import Flask, url_for, request, g, jsonify
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
	return jsonify(new_loc.jsonify())


@app.route('/locations', methods=['GET'])
@app.route('/locations/<int:location_id>', methods=['GET'])
def readLocation(location_id=None):
	app.logger.debug("In readLocation - GET request")
	resultJSON = {}
	if (location_id == None):
		# get all 
		read_loc = g.session.query(Location).all()
		if (read_loc == None):
			app.logger.warning("No entries in database")
			resultJSON['status'] = 'fail'
			resultJSON['results'] = []
			return jsonify(resultJSON)
	else:
		# get specific location_id
		read_loc = g.session.query(Location).get(location_id)
		if (read_loc == None):
			app.logger.warning("Internal warning: No such ID in db")
			resultJSON['status'] = 'fail'
			resultJSON['results'] = []
			return jsonify(resultJSON)
		read_loc = [read_loc]

	lstJSON = []
	for loc in read_loc:
		lstJSON.append(loc.jsonify())
	resultJSON['results'] = lstJSON
	resultJSON['status'] = "success"
	app.logger.info("Got existing location(s)")
	return jsonify(resultJSON)

@app.route('/locations/<int:location_id>', methods=['PUT'])
def updateLocation(location_id=None):
	app.logger.debug("In updateLocation - PUT request")
	resultJSON = {}
	if (location_id == None):
		app.logger.error("Request Format Error: No id in update request")
		resultJSON['status'] = 'fail'
		return jsonify(resultJSON)

	loc_obj = g.session.query(Location).get(location_id)
	if (loc_obj == None):
		app.logger.warning("Internal warning: No such ID in db")
		resultJSON['status'] = 'fail'
		return jsonify(resultJSON)
	
	# get all the things to update, and update them
	loc_obj.name = request.form['name']
	loc_obj.address = request.form['address']
	loc_obj.lng = request.form['lng']
	loc_obj.lat = request.form['lat']
	
	app.logger.info("Updated existing location - id: " + str(location_id))
	resultJSON['status'] = 'success'
	return jsonify(resultJSON)

@app.route('/locations/<int:location_id>', methods=['DELETE'])
def deleteLocation(location_id=None):
	app.logger.debug("In deleteLocation - DELETE request")
	resultJSON = {}
	if (location_id == None):
		app.logger.error("Request Format Error: No id in delete request")
		resultJSON['status'] = 'fail'
		return jsonify(resultJSON)

	loc_obj = g.session.query(Location).get(location_id)
	if (loc_obj == None):
		app.logger.warning("Internal warning: No such ID in db")
		resultJSON['status'] = 'fail'
		return jsonify(resultJSON)

	loc_obj.delete()
	app.logger.info("Success: Deleted existing location - id: " + str(location_id))
	resultJSON['status'] = 'success'
	return jsonify(resultJSON)

if __name__ == '__main__':
	app.run(debug=True)