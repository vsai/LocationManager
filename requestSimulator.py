import requests

url = "http://localhost:5000/locations"
#simulate GET request for ID
def req_GET_id(idNum):
	url2 = url + "/" + str(idNum)
	r = requests.get(url2)
	print r
	print r.json()
	return r.json()

def req_GET_all():
	r = requests.get(url)
	print r
	print r.json()
	return r.json()

def req_POST_id(name, address, lng, lat):
	payload = {'name' : name, 'address' : address, 'lng' : lng, 'lat' : lat}
	r = requests.post(url, data=payload)
	print r
	print r.json()
	return r.json()

def req_UPDATE_id(idNum, name, address, lng, lat):
	url2 = url + "/" + str(idNum)
	payload = {'name' : name, 'address' : address, 'lng' : lng, 'lat' : lat}
	r = requests.put(url2, data=payload)
	print r
	print r.json()
	return r.json()

def req_DELETE_id(idNum):
	url2 = url + "/" + str(idNum)
	r = requests.delete(url2)
	print r
	print r.json()
	return r.json()

# req_UPDATE_id(12, 'vishalsai', '39 carnarvon road', '111', '222')
# req_DELETE_id(15)
# req_POST_id('vishalsai', '39 carnarvon road', '111', '222')
# req_GET_id(100)
# req_GET_all()	

