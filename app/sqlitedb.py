import web

db = web.database(dbn='sqlite', db='RestaurantsOld.db')

# Enforce foreign key constraints
# WARNING: DO NOT REMOVE THIS!
def enforceForeignKey():
    db.query('PRAGMA foreign_keys = ON')

# initiates a transaction on the database
def transaction():
    return db.transaction()

# wrapper method around web.py's db.query method
# check out http://webpy.org/cookbook/query for more info
def query(query_string, vars = {}):
    return list(db.query(query_string, vars))

def getReviewsByRestaurant(restaurantId):
    query_str = 'select * from Reviews where RestaurantID = $restaurantId'
    result = query(query_str, {'restaurantId': restaurantId})
    if result:
        return result
    else:
        return

def getRestaurantById(restaurantId):
    # TODO: rewrite this method to catch the Exception in case `result' is empty
    query_string = 'select * from Restaurants where RestaurantID = $restaurantId'
    result = query(query_string, {'restaurantId': restaurantId})
    #print result, item_id, query_string
    if result:
        #print "returning result", result[0]
        return result[0]
    else:
        #print "returning none"
        return

# category is not array
# check if any param is null to not add to the query
# calculate distance limit via long/lat conversion ---> post query
# filtering (may have large result set to filter through)
def search(restaurantId, name, category, minPrice, maxPrice, city, lat, longi, distance, minStars, numResults):
    queryStr = 'select distinct r.RestaurantId, r.Name, r.Price, r.City, r.Rating from Restaurants as r, Categories as c'

    if lat and longi and distance:
        queryStr = 'select distinct (((abs(r.Latitude - $lat)*abs(r.Latitude - $lat))+(abs(r.Longitude - $longi)*abs(r.Longitude - $longi)))*69*69) as dist, r.RestaurantId, r.Name, r.Price, r.City, r.Rating from Restaurants as r, Categories as c'
    conditionCount = 0
    
    if minStars:
        minStarsInt = int(minStars)
        if(conditionCount > 0):
            queryStr += ' and '
        else:
            queryStr += ' where '
            queryStr += 'r.Rating >= $minStars'
        conditionCount += 1

    #queryStr += ' limit 5'
    #searchResult = query(queryStr, {'minStars': minStarsInt})
    #return searchResult

    if restaurantId:
        if(conditionCount > 0):
            queryStr += ' and '
        else:
            queryStr += ' where '
        queryStr += 'r.RestaurantID = $restaurantId'
        conditionCount += 1

    if category:
        if(conditionCount > 0):
            queryStr += ' and '
        else:
            queryStr += ' where '
        queryStr += 'c.RestaurantID = r.RestaurantID and c.Category = $category'
        conditionCount += 1

    if name:
        if(conditionCount > 0):
            queryStr += ' and '
        else:
            queryStr += ' where '
        queryStr += 'r.Name = $name'
        conditionCount += 1

    if minPrice:
        if(conditionCount > 0):
            queryStr += ' and '
        else:
            queryStr += ' where '
        queryStr += 'r.Price >= $minPrice'
        conditionCount += 1

    if maxPrice:
        if(conditionCount > 0):
            queryStr += ' and '
        else:
            queryStr += ' where '
        queryStr += 'r.Price <= $maxPrice'
        conditionCount += 1


    if city:
        if(conditionCount > 0):
            queryStr += ' and '
        else:
            queryStr += ' where '
        queryStr += 'r.City = $city'
        conditionCount += 1


    distanceSq = 1000
    if lat and longi and distance:
        #print lat, longi, distance
        distanceSq = float(distance)*float(distance)
        if(conditionCount > 0):
            queryStr += ' and '
        else:
            queryStr += ' where '
        # a = abs(lat1-lat2) b = abs(long1-long2)
        # 69* sqrt(a2+b2) <= distance
        # a2+b2 <= (distance/69)^2 = distance*distance/(69*69)
        queryStr += '(((abs(r.Latitude - $lat)*abs(r.Latitude - $lat))+(abs(r.Longitude - $longi)*abs(r.Longitude - $longi)))*69*69) <= $distanceSq'
        conditionCount += 1
        #queryStr += ' order by dist'
        if numResults:
            queryStr += ' limit $numResults'
        else:
            queryStr += ' limit 50'
        nestedQueryStr = 'select * from ('+queryStr+') order by dist'
        #print queryStr
        searchResult = query(nestedQueryStr, {'restaurantId': restaurantId, 'category': category, 'name': name,
                                        'minPrice': minPrice, 'maxPrice':
                                        maxPrice, 'city': city, 'minStars':
                                        minStarsInt, 'lat': float(lat), 'longi': float(longi),
                                        'distanceSq': distanceSq, 'numResults': numResults})
        return searchResult

    if numResults:
        queryStr += ' limit $numResults'
    else:
        queryStr += ' limit 50'
    searchResult = query(queryStr, {'restaurantId': restaurantId, 'category': category, 'name': name,
                                    'minPrice': minPrice, 'maxPrice':
                                    maxPrice, 'city': city,
                                    'minStars':minStarsInt, 'numResults': numResults})
    return searchResult

def getCategories(restaurantId):
    queryStr = 'select distinct Category from Categories where RestaurantId = $restaurantId'
    results = query(queryStr, {'restaurantId': restaurantId})
    if results:
        return results
    else:
        return

def getAllCategories():
    queryStr = 'select distinct Category from Categories order by Category'
    results = query(queryStr)
    if results:
        return results
    else:
        return
