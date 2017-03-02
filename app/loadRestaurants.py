import json

def get(filename):
	data = {}
	fd = open(filename, 'r')
	data = json.load(fd)
	return data

#restaurant object: {'name': name, 'id': rid, 'city': city, 'latitude': latitude, 'longitude': longitude, 'price': price, 'categories': categories}
def main():
	restaurants = get('restaurantsJson.txt')
	#do stuff with loaded restaurants here
	#restaurants[0]['name'] is name of first restaurant in list
	

if __name__=="__main__":
	main()