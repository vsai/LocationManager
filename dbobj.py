#db objects

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

#settings
table_names = {'fav_loc_tbl' : 'locations', 'usr_tbl' : 'users'}

Base = declarative_base()

class Location(Base):
	__tablename__ = table_names.get('fav_loc_tbl')

	id = Column(Integer, primary_key=True)
	#lengths of name, latitude, longitude are restricted
	name = Column(String(30))
	address = Column(String)
	lat = Column(String(20))
	lng = Column(String(20))

	# def __init__(self, name, address, lat, lng):
	# 	self.name = name
	# 	self.address = address
	# 	self.lat = lat
	# 	self.lng = lng

	def __repr__(self):
		return "<Location('%s', '%s', '%s', '%s')>" % (self.name, self.address, self.lat, self.lng)

class User(Base):
	__tablename__ = table_names.get('usr_tbl')

	id = Column(Integer, primary_key=True)
	name = Column(String)
	pwd = Column(String)

	def __init__(self, name, pwd):
		self.name = name
		self.pwd = pwd

	def __repr__(self):
		return "<User('%s')> " % (self.name)