from flask import Flask, url_for, request, g, jsonify, abort, make_response
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import *
from customErrors import *

engine = create_engine('postgresql://vishalsaidaswani@localhost/myfirstdb')
Base.metadata.create_all(engine)
Session = sessionmaker(bind = engine)
app = Flask(__name__)

app.logger.setLevel('DEBUG')
# app.logger.setLevel('INFO')
# app.logger.setLevel('WARNING')

app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False

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
	g.session.close()
	if exception:
		app.logger.error("fail - Thrown exception")

@app.errorhandler(UberError)
def custom_uberrror(error):
	print "HELLO"
	x = {404 : 'Not found', 400 : 'Bad request', 500 : 'Internal server error', 200: 'OK'}
	return make_response(jsonify( { 'status':'error', 'error': x[error.num], 'message': error.message } ), error.num)

# @app.errorhandler(404)
# def custom_401(error):
# 	app.logger.error("Error handler 404")
# 	print error
# 	return make_response(jsonify( { 'status':'error', 'error': 'Not found' } ), 404)

# @app.errorhandler(400)
# def custom_400(error):
# 	app.logger.error("Error handler 400")
# 	return make_response(jsonify( { 'status':'error', 'error': 'Bad Request' } ), 404)

@app.route('/')
def hello_world():
	return 'Hello World!'

@app.route('/locations', methods=['POST'])
def createLocation():
	app.logger.debug("In createLocation - POST request")
	x = request.form
	try:
		(lname, laddress, llat, llng) = (x['name'], x['address'], x['lat'], x['lng'])
	except:
		raise UberError(400, 'form does not include all necessary fields - name, address, lat, lng')
	new_loc = Location(name = lname, address = laddress, lat = llat, lng = llng)
	g.session.add(new_loc)
	g.session.flush()
	assert(new_loc.id >= 1)
	app.logger.info("Created new location - id: " + str(new_loc.id))
	resultJSON = new_loc.jsonify()
	return make_response(jsonify( { 'results':resultJSON, 'status': 'OK' } ), 200)

@app.route('/locations', methods=['GET'])
def readAllLocations():
	app.logger.debug("In readAllLocations - GET request")
	read_loc = g.session.query(Location).all()
	if not read_loc:
		app.logger.warning("No entries in database")
		raise UberError(404, "No entries found")
	lstJSON = []
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
	return make_response(jsonify( { 'results':[read_loc.jsonify()], 'status': 'OK' } ), 200)

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
	x = request.form
	try:
		(loc_obj.name, loc_obj.address, loc_obj.lat, loc_obj.lng) = (x['name'], x['address'], x['lat'], x['lng'])
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