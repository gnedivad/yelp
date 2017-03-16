from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from random import shuffle
from random import choice
import json
import math

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 


def loadBusinessVectors():
	bvectors = open('./data/businessAdjectiveVectors.txt')
	return json.load(bvectors)

def loadUserReviews():
	return json.load(open('./data/uidToReviews.txt'))

def getXY(userReviewList, businessVectors):
	try:
		XU = [businessVectors[userReviewObj['bid']] for userReviewObj in userReviewList]
		YU = [userReviewObj['stars'] for userReviewObj in userReviewList]
		indices = range(len(XU))
		shuffle(indices)
		X = [XU[i] for i in indices]
		Y = [YU[i] for i in indices]
		return X,Y
	except:
		return 'error',''


def knnEval(userReviews, businessVectors):
	numErrors = 0
	absError = 0
	numPred = 0
	for user in userReviews:
		if (len(userReviews[user]) >= 50):
			X, Y = getXY(userReviews[user], businessVectors)
			#a few reviews had exceptions
			if (X=='error'):
				numErrors +=1
			else:
				for i in range(len(userReviews[user])):
					if (numPred % 10000 == 0):
						print "Num pred so far: " + str(numPred)

					#tested with representative sample, 50k/~400k reviews
					if (numPred == 50000):
						print('Avg error: ' + str(float(absError)/numPred))
						return

					xTest = X[i: i+1]
					yTest = Y[i: i+1]
					xTrain = X[:]
					yTrain = Y[:]
					del xTrain[i]
					del yTrain[i]
					neigh = KNeighborsClassifier(n_neighbors=1)
					neigh.fit(xTrain, yTrain)
					val = neigh.predict(xTest[0])
					absError += abs(val-yTest[0])
					numPred += 1	

	#writes if terminating condition of 50k reviews is removed
	print('Avg error for knn: ' + str(float(absError)/numPred))


import random
def random_pick(some_list, probabilities):
    x = random.uniform(0, 1)
    cumulative_probability = 0.0
    for item, item_probability in zip(some_list, probabilities):
        cumulative_probability += item_probability
        if x < cumulative_probability: break
    return item

def randomEval(userReviews, uniform):
	absMiss = 0
	numPred = 0
	allRatings = []
	possibleRatings = [1,2,3,4,5]
	for user in userReviews:
		reviews = userReviews[user]
		stars = [review['stars'] for review in reviews if not math.isnan(review['stars'])]
		allRatings.extend(stars)
	print len(allRatings)
	probabilities = [allRatings.count(i)/float(len(allRatings)) for i in range(1,6)]
	print probabilities
	for star in allRatings:
		if not star in possibleRatings:
			print type(star)
			print star
	for rating in allRatings:
		if (uniform == True):
			randVal = choice(possibleRatings)
		else:
			randVal = random_pick(possibleRatings, probabilities)
		absMiss += abs(randVal - rating)
		numPred += 1
	if (uniform):
		print ('Avg error for uniform random evaluation: ' + str(float(absMiss)/numPred))
	else:
		print ('Avg error for random evaluation over the distribution of ratings: ' + str(float(absMiss)/numPred))


#Results:
#Avg error for knn:.982
#Avg error for uniform random evaluation: 1.65249924533
#Avg error for random evaluation over the distribution of ratings: 1.43382720974


def main():
	userReviews = loadUserReviews()
	businessVectors = loadBusinessVectors()
	#knnEval(userReviews, businessVectors)
	randomEval(userReviews, True)
	randomEval(userReviews, False)


if __name__=="__main__":
	main()
