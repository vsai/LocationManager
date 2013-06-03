from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Schedule(Base):
	__tablename__ = 'tbl_locations'

	id = Column(Integer, primary_key=True)
	#lengths of name, latitude, longitude are restricted
	user_id = Column(Integer)
	# name = Column(String(30))
	address = Column(String)
	latitude = Column(String(20))
	longitude = Column(String(20))
	schedule_time = Column(DateTime)

	def jsonify(self):
		r = {}
		r['id'] = self.id
		r['user_id'] = self.user_id
		r['address'] = self.address
		r['latitude'] = self.latitude
		r['longitude'] = self.longitude
		r['schedule_time'] = self.schedule_time
		return r

	def __repr__(self):
		return "<Location('%d', '%s', '%s', '%s', '%s')>" % (self.id, self.name, self.address, self.latitude, self.longitude)