from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Location(Base):
	__tablename__ = 'tbl_locations3'

	id = Column(Integer, primary_key=True)
	#lengths of name, latitude, longitude are restricted
	name = Column(String(30))
	address = Column(String)
	latitude = Column(String(20))
	longitude = Column(String(20))

	def jsonify(self):
		r = {}
		r['id'] = self.id
		r['name'] = self.name
		r['address'] = self.address
		r['latitude'] = self.latitude
		r['longitude'] = self.longitude
		return r

	def __repr__(self):
		return "<Location('%d', '%s', '%s', '%s', '%s')>" % (self.id, self.name, self.address, self.latitude, self.longitude)