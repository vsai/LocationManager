# #database api

# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import create_engine
# from dbobj import *

# engine = create_engine('postgresql://vishalsaidaswani@localhost/myfirstdb')
# Base.metadata.create_all(engine)
# Session = sessionmaker(bind = engine)

# def createLocation(lname, laddress, llat, llng):
# 	new_loc = Location(name = lname, address = laddress, lat = llat, lng = llng)
# 	session = Session()
# 	session.add(new_loc)
# 	session.commit()
# 	return True

# def readLocation():
# 	pass

# def updateLocation():
# 	pass

# def deleteLocation():
# 	pass

# def createUser(lname, lpwd):
# 	new_user = User(lname, lpwd)
# 	session = Session()
# 	session.add(new_user)
# 	session.commit()
# 	return True

# def readUser():
# 	pass

# def updateUser():
# 	pass

# def deleteUser():
# 	pass
