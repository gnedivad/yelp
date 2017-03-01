import json
import numpy as np
import operator
from collections import defaultdict


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
  category city name price stars
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

  star_to_col_offset = price_to_col_offset + len(prices)
  for i, star in enumerate(stars):
    star_to_col[star[0]] = i + star_to_col_offset

  num_rows = len(restaurants)
  num_cols = star_to_col_offset + len(stars)
  A = np.zeros((num_rows, num_cols))
  for i, restaurant in enumerate(restaurants):
    cols = []
    for category in restaurant["categories"]:
      cols.append(category_to_col[category])
    cols.append(city_to_col[restaurant["city"]])
    cols.append(name_to_col[restaurant["name"]])
    cols.append(price_to_col[restaurant["price"]])
    cols.append(star_to_col[restaurant["stars"]])

    A[i, cols] = 1

  return A


def k_nearest_neighbor():
  pass


def main():
  with open("data/restaurants.json", "rb") as f:
    restaurants = json.load(f)
  info = count_restaurants(restaurants)
  A = vectorize_restaurants(restaurants, info)
  import pdb; pdb.set_trace()


if __name__=="__main__":
  main()
