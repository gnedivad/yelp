import json
import operator
from collections import defaultdict


def count_restaurants(restaurants):
  """
  Aggregates counts of restaurants for various features.

  Inputs:
  - restaurants: A list of dicts mapping city, name, price, longitude,
    latitude, stars, id, and categories to their values.
  """
  cities = defaultdict(int)
  names = defaultdict(int)
  categories = defaultdict(int)
  for restaurant in restaurants:
    cities[restaurant["city"]] += 1
    names[restaurant["name"]] += 1
    for category in restaurant["categories"]:
      categories[category] += 1
  sorted_cities = sorted(
    cities.items(), key=operator.itemgetter(1), reverse=True)
  sorted_names = sorted(
    names.items(), key=operator.itemgetter(1), reverse=True)
  sorted_categories = sorted(
    categories.items(), key=operator.itemgetter(1), reverse=True)
  import pdb; pdb.set_trace()


def main():
  with open("data/restaurants.json", "rb") as f:
    restaurants = json.load(f)
  count_restaurants(restaurants)


if __name__=="__main__":
  main()
