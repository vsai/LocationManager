#flask end points

from flask import Flask
from dbapi import *

app = Flask(__name__)


# @app.before_request
# def before_request():
# 	print "Before Request"
#     # g.db = connect_db()

# @app.after_request
# def after_request():
# 	print "After request"

# @app.teardown_request
# def teardown_request(exception):
# 	print "Teardown Request"
#     # g.db.close()


@app.route('/')
def hello_world():
	# print 'hello world'
	return 'Hello World!'

@app.route('/create/')
def createLocation():
	print "CREATING"
	createLocation('Work', '405 Howard Street, San Francisco, CA', 'def1', 'def2')
	return 'Created'

if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host = '0.0.0.0') #to listen on all public ips