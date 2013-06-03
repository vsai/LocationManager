from flask import Flask, url_for, request, g, jsonify, abort, make_response, render_template
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import *
from customErrors import *
import json


app = Flask(__name__)
app.logger.setLevel('INFO')
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False

#initialize database
engine = create_engine('postgresql://vishalsaidaswani@localhost/locationManager')
Base.metadata.create_all(engine)
Session = sessionmaker(bind = engine)


@app.before_request
def before_request():
	app.logger.debug("Before Request")
	if (request.endpoint != 'hello_world'):
		g.session = Session()

@app.after_request
def after_request(response):
	app.logger.debug("After Request")
	if (request.endpoint != 'hello_world'):
		g.session.commit()
	return response

@app.teardown_request
def teardown_request(exception):
	app.logger.debug("Teardown Request")
	if (request.endpoint != 'hello_world'):
		g.session.close()
	if exception:
		app.logger.error(exception)
		app.logger.error("fail - Thrown exception")

@app.errorhandler(UberError)
def custom_uberrror(error):
	x = {404 : 'Not found', 400 : 'Bad request', 500 : 'Internal server error', 200: 'OK'}
	return make_response(jsonify( { 'status':'error', 'error': x[error.num], 'message': error.message } ), error.num)

@app.route('/')
def hello_world():
	# return render_template('editabletest.html')
	return render_template('test.html')

@app.route('/locations', methods=['POST'])
def createLocation():
	app.logger.debug("In createLocation - POST request")
	# print request.data
	x = json.loads(request.data)
	try:
		(lname, laddress, llat, llng) = (x['name'], x['address'], x['latitude'], x['longitude'])
	except:
		raise UberError(400, 'form does not include all necessary fields - name, address, lat, lng')
	new_loc = Location(name = lname, address = laddress, latitude = llat, longitude = llng)
	g.session.add(new_loc)
	g.session.flush()
	assert(new_loc.id >= 1)
	app.logger.info("Created new location - id: " + str(new_loc.id))
	resultJSON = new_loc.jsonify()
	return make_response(jsonify( {'id':new_loc.id} ), 200)
	# return make_response(jsonify( { 'results':resultJSON, 'status': 'OK' } ), 200)

@app.route('/locations', methods=['GET'])
def readAllLocations():
	app.logger.debug("In readAllLocations - GET request")
	read_loc = g.session.query(Location).all()
	lstJSON = []
	if not read_loc:
		app.logger.warning("No entries in database")
		return make_response(jsonify( { 'results':lstJSON, 'status': 'OK' } ), 200)
	for loc in read_loc:
		lstJSON.append(loc.jsonify())
	app.logger.info("Got existing location(s)")
	return make_response(jsonify( { 'results':lstJSON, 'status': 'OK' } ), 200)

@app.route('/locations/<int:location_id>', methods=['GET'])
def readLocation(location_id=None):
	app.logger.debug("In readLocation - GET request")
	if not location_id:
		raise UberError(400, "Missing location_id parameter")
	# get specific location_id
	read_loc = g.session.query(Location).get(location_id)
	if not read_loc:
		app.logger.warning("Internal warning: No such ID in db")
		raise UberError(404, "ID not found in database")
	app.logger.info("Got existing location(s)")
	return make_response(jsonify( { 'results':read_loc.jsonify(), 'status': 'OK' } ), 200)

@app.route('/locations/<int:location_id>', methods=['PUT'])
def updateLocation(location_id=None):
	app.logger.debug("In updateLocation - PUT request")
	resultJSON = {}
	if not location_id:
		app.logger.error("Request Format Error: No id in update request")
		raise UberError(400, "Missing location_id parameter")
	loc_obj = g.session.query(Location).get(location_id)
	if not loc_obj:
		app.logger.warning("Internal warning: No such ID in db")
		raise UberError(404, "ID not found in database")
	x = json.loads(request.data)
	try:
		(loc_obj.name, loc_obj.address) = (x['name'], x['address'])
		(loc_obj.latitude, loc_obj.longitude) = (x['latitude'], x['longitude'])
	except:
		raise UberError(400, 'form does not include all necessary fields - name, address, lat, lng')
	app.logger.info("Updated existing location - id: " + str(location_id))
	return make_response(jsonify( { 'status': 'OK' } ), 200)

@app.route('/locations/<int:location_id>', methods=['DELETE'])
def deleteLocation(location_id=None):
	app.logger.debug("In deleteLocation - DELETE request")
	resultJSON = {}
	if not location_id:
		app.logger.error("Request Format Error: No id in delete request")
		raise UberError(400, "Missing location_id parameter")
	loc_obj = g.session.query(Location).get(location_id)
	if not loc_obj:
		app.logger.warning("Internal warning: No such ID in db")
		raise UberError(404, "ID not found in database")
	g.session.delete(loc_obj)
	app.logger.info("Success: Deleted existing location - id: " + str(location_id))
	return make_response(jsonify( { 'status': 'ok' } ), 200)

if __name__ == '__main__':
	app.run(debug=True)