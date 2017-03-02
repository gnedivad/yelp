import json

columnSeparator = "|"
quote = "\""

def get(filename):
	data = {}
	fd = open(filename, 'r')
	data = json.load(fd)
	return data

#restaurant object: {'name': name, 'id': rid, 'city': city, 'latitude': latitude, 'longitude': longitude, 'price': price, 'categories': categories}
# other attributes restaurant may have include rating, open hours, etc
# we model the user preference based on the user input form for filtring, but not saving the data
def main():
	restaurants = get('restaurantsJson.txt')
	#do stuff with loaded restaurants here
	#restaurants[0]['name'] is name of first restaurant in list
	restaurantFile = open('restaurants.dat', 'w')
	categoriesFile = open('categories.dat', 'w')

	# overwrite the old file
	restaurantFile.seek(0)
	categoriesFile.seek(0)

	for r in restaurants:
		line = quote + r['id'].replace('\"','\"\"') + quote +\
		columnSeparator + quote + r['name'].replace('\"','\"\"') + quote +\
		columnSeparator + quote + r['city'].replace('\"','\"\"') + quote +\
		columnSeparator + str(r['latitude']) +\
		columnSeparator + str(r['longitude']) +\
		columnSeparator + str(r['price']) +\
		columnSeparator + str(r['stars'])
                #print line
		restaurantFile.write(line.encode('utf-8'))
		restaurantFile.write('\n')

		for c in r['categories']:
			cLine = quote + r['id'].replace('\"','\"\"') + quote +\
			columnSeparator + quote + c.replace('\"','\"\"') + quote
			categoriesFile.write(cLine.encode('utf-8'))
			categoriesFile.write('\n')

	restaurantFile.close()
	categoriesFile.close()

if __name__=="__main__":
	main()
