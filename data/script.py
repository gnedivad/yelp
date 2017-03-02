import json

def filter_reviews():
  """
  Filters reviews, which will be read from models/stars_from_metadata.py.
  """
  with open("yelp_dataset_challenge_round9/yelp_academic_dataset_review.json", "rb") as f:
    filtered_reviews = []
    for i, line in enumerate(f):
      review = json.loads(line)
      filtered_reviews.append({
        "user_id": review["user_id"],
        "business_id": review["business_id"],
        "stars": review["stars"],
      })

  with open("reviews_stars.json", "wb") as f:
    json.dump(filtered_reviews, f)

def main():
  filter_reviews()

if __name__ == "__main__":
  main()
