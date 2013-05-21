#postgres database connection test
from sqlalchemy import *

#dialect+driver://username:password@host:port/database
db = create_engine('postgresql://vishalsaidaswani@localhost/myfirstdb')
conn = db.connect()
result = conn.execute("select * from users")
for row in result:
	print row
	# print "name:", row['name']
conn.close()
