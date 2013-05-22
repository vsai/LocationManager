from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Location(Base):
	__tablename__ = 'tbl_locations'

	id = Column(Integer, primary_key=True)
	#lengths of name, latitude, longitude are restricted
	name = Column(String(30))
	address = Column(String)
	lat = Column(String(20))
	lng = Column(String(20))

	def __repr__(self):
		return "<Location('%s', '%s', '%s', '%s')>" % (self.name, self.address, self.lat, self.lng)