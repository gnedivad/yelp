from __future__ import division
import json
import numpy as np
import operator
import sys
from collections import defaultdict
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.neighbors import NearestNeighbors


def count_restaurants(restaurants):
  """
  Aggregates counts of restaurants for various features.
  - There are 668 distinct cities including Toronto (6231), Las Vegas (5379),
    and Phoenix (3327).
  - There are 33591 distinct names including McDonald's (588), Subway (520),
    and Taco Bell (257).
  - There are 149 sorted categories including Food (8451), Nighlife (6285),
    and Bars (6023).

  Inputs:
  - restaurants: A list of dicts mapping city, name, price, longitude,
    latitude, stars, id, and categories to their values.
  """
  categories = defaultdict(int)
  cities = defaultdict(int)
  names = defaultdict(int)
  prices = defaultdict(int)
  stars = defaultdict(int)
  for restaurant in restaurants:
    for category in restaurant["categories"]:
      categories[category] += 1
    cities[restaurant["city"]] += 1
    names[restaurant["name"]] += 1
    prices[restaurant["price"]] += 1
    stars[restaurant["stars"]] += 1
  sorted_categories = sorted(
    categories.items(), key=operator.itemgetter(1), reverse=True)
  sorted_cities = sorted(
    cities.items(), key=operator.itemgetter(1), reverse=True)
  sorted_names = sorted(
    names.items(), key=operator.itemgetter(1), reverse=True)
  sorted_prices = sorted(
    prices.items(), key=operator.itemgetter(0))
  sorted_stars = sorted(
    stars.items(), key=operator.itemgetter(0))
  return (
    sorted_categories,
    sorted_cities,
    sorted_names,
    sorted_prices,
    sorted_stars,
  )


def vectorize_restaurants(restaurants, info):
  """
  Vectorizes restaurants with the following column ordering:
  - X = category | city | name | price; categories, cities, and names ordered
    by number of occurences while price ordered from lower prices to higher
    prices.
  - y = stars; ordered from lower stars to higher stars.

  Also returns:
  - restaurant_id_to_row_index: pretty self-explanatory; a dict mapping
    restaurant ids to the row indices in X and y.
  """
  categories, cities, names, prices, stars = info
  category_to_col, city_to_col, name_to_col, price_to_col, star_to_col = \
    {}, {}, {}, {}, {}

  category_to_col_offset = 0
  for i, category in enumerate(categories):
    category_to_col[category[0]] = i + category_to_col_offset

  city_to_col_offset = category_to_col_offset + len(categories)
  for i, city in enumerate(cities):
    city_to_col[city[0]] = i + city_to_col_offset

  name_to_col_offset = city_to_col_offset + len(cities)
  for i, name in enumerate(names):
    name_to_col[name[0]] = i + name_to_col_offset

  price_to_col_offset = name_to_col_offset + len(names)
  for i, price in enumerate(prices):
    price_to_col[price[0]] = i + price_to_col_offset

  num_rows = len(restaurants)
  num_cols = price_to_col_offset + len(prices)
  X = np.zeros((num_rows, num_cols))
  for i, restaurant in enumerate(restaurants):
    cols = []
    for category in restaurant["categories"]:
      cols.append(category_to_col[category])
    cols.append(city_to_col[restaurant["city"]])
    cols.append(name_to_col[restaurant["name"]])
    cols.append(price_to_col[restaurant["price"]])

    X[i, cols] = 1

  star_to_col_offset = 0
  for i, star in enumerate(stars):
    star_to_col[star[0]] = i + star_to_col_offset

  num_rows = len(restaurants)
  num_cols = len(stars)
  y = np.zeros((num_rows, num_cols))
  for i, restaurant in enumerate(restaurants):
    star_col = star_to_col[restaurant["stars"]]

    y[i, star_col] = 1

  restaurant_id_to_row_index = {}
  for i, restaurant in enumerate(restaurants):
    restaurant_id_to_row_index[restaurant["id"]] = i

  return X, y, restaurant_id_to_row_index


def group_reviews_by_user(reviews):
  """
  Each user has an average of 4.0344 (restaurant and non-restaurant) reviews.

  537904 have 1 review.
  171046 have 2 reviews.
  88508 have 3 reviews.
  52877 have 4 reviews.
  34820 have 5 reviews.
  247735,  18214,  14253,  11268,   8761,
    7457,   6064,   5103,   4378,   3808,
    3259,   2823,   2495,   2251,   1908 have 6-20 reviews.
  """
  user_to_reviews = defaultdict(list)
  for review in reviews:
    user_to_reviews[review["user_id"]].append({
      "business_id": review["business_id"],
      "stars": review["stars"],
    })
  return user_to_reviews


def random_guessing(X, y, rest_id_to_row_index, user_to_reviews):
  """
  Yields a average loss of around 1.11 buckets (0.555 stars).

  A uniform distribution of stars across all buckets yields a average loss of
  around 240/81 = 2.96 buckets (1.481 stars).
  """
  losses = []
  running_sum = 0
  running_count = 0
  previous_loss = 0
  for i, (user, reviews) in enumerate(user_to_reviews.iteritems()):
    if i % 1000 == 0 and i != 0:
      loss = running_sum / running_count
      print i, "out of", len(user_to_reviews), "| loss:", loss
      if abs(previous_loss - loss) < 0.005:
        return loss
      previous_loss = loss
      sys.stdout.flush()
    if len(reviews) < 50:
      continue
    # User might have reviewed a non-restaurant business, which
    # rest_id_to_row_index doesn't know about.
    row_indices = [
      rest_id_to_row_index[review["business_id"]] for review in reviews \
        if review["business_id"] in rest_id_to_row_index
    ]
    # Filtering out non-restaurant businesses might reduce the number of
    # reviews for a particular user below 10.
    if len(row_indices) < 50:
      continue

    X_sub = X[row_indices,]
    y_sub = y[row_indices,]
    indices = np.hstack((
      np.expand_dims(np.arange(len(row_indices)), axis=1),
      np.expand_dims(np.random.randint(0, len(row_indices), len(row_indices)), axis=1)
    ))
    A = np.where(y_sub[indices] == 1)[2]
    loss = np.mean(np.abs(A[::2] - A[1::2]))
    # np.mean(np.square(A[::2] - A[1::2]))
    losses.append(loss)
    running_sum += loss
    running_count += 1


def k_nearest_neighbor(X, y, rest_id_to_row_index, user_to_reviews):
  """
  Yields a average loss of around 1.01 buckets (0.505 stars) for a threshold
  of 50 reviews.

  +-----------+----------+
  | Threshold |   Loss   |
  +-----------+----------+
  |     10    |   1.09   |
  |     25    |   1.07   |
  |     50    |   1.01   |
  |     75    |   0.96   |
  +-----------+----------+
  """
  losses = []
  running_sum = 0
  running_count = 0
  previous_loss = 0
  for i, (user, reviews) in enumerate(user_to_reviews.iteritems()):
    if i % 1000 == 0 and i != 0 and running_count > 0:
      loss = running_sum / running_count
      print i, "out of", len(user_to_reviews), "| loss:", loss
      if abs(previous_loss - loss) < 0.001:
        return loss
      previous_loss = loss
      sys.stdout.flush()
    if len(reviews) < 75:
      continue
    # User might have reviewed a non-restaurant business, which
    # rest_id_to_row_index doesn't know about.
    row_indices = [
      rest_id_to_row_index[review["business_id"]] for review in reviews \
        if review["business_id"] in rest_id_to_row_index
    ]
    # Filtering out non-restaurant businesses might reduce the number of
    # reviews for a particular user below 10.
    if len(row_indices) < 75:
      continue

    X_sub = X[row_indices,]
    y_sub = y[row_indices,]
    nbrs = NearestNeighbors(n_neighbors=2, algorithm='ball_tree')\
      .fit(X_sub)
    distances, indices = nbrs.kneighbors(X_sub)

    # For each review, determines the number of stars-buckets between the
    # review and its nearest neighbor. For example, if a review had 2.5 stars
    # and its nearest neighbor had 3.5 stars, then this would contribute 2 to
    # the loss (since the 3.5 bucket is 2 buckets away from the 2.5 bucket).
    A = np.where(y_sub[indices] == 1)[2]
    loss = np.mean(np.abs(A[::2] - A[1::2]))
    # np.mean(np.square(A[::2] - A[1::2]))
    losses.append(loss)
    running_sum += loss
    running_count += 1


def softmax_regression(X, y, rest_id_to_row_index):  #, user_to_reviews):
  """
  Yields an average loss of around 1.05 buckets (0.526 stars) using just
  business data (no user reviews data).
  """
  y = np.where(y == 1)[1]
  X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42)
  classifier = LogisticRegression()  # softmax classifier
  classifier.fit(X_train, y_train)
  predictions = classifier.predict(X_test)
  loss = np.mean(np.abs(predictions - y_test))
  return loss


def main():
  with open("data/restaurants.json", "rb") as f:
    restaurants = json.load(f)
  info = count_restaurants(restaurants)
  X, y, rest_id_to_row_index = vectorize_restaurants(restaurants, info)

  """
  with open("data/reviews_stars.json", "rb") as f:
    reviews = json.load(f)
  user_to_reviews = group_reviews_by_user(reviews)

  knn_loss = k_nearest_neighbor(X, y, rest_id_to_row_index, user_to_reviews)
  print "knn_loss:", knn_loss

  print "-" * 60
  rand_loss = random_guessing(X, y, rest_id_to_row_index, user_to_reviews)
  print "rand_loss:", rand_loss
  """

  print "-" * 60
  softmax_loss = softmax_regression(X, y, rest_id_to_row_index)
  print "softmax_loss:", softmax_loss


if __name__=="__main__":
  main()
