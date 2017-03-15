#import pandas as pd
#import gzip
import json

#review = pd.read_csv('review.tsv.gz',sep='\t')
#print review[0]
#for data in review[0]:
#    print data
#subset = review.loc([1])
#print subset

columnSeparator = "|"
quote = "\""

def get(filename):
    data = {}
    fd = open(filename, 'r')
    data = json.load(fd)
    return data

def main():
    reviews = get('review.json')
    #print reviews["business_id"]["32"]
    #print reviews["text"]["32"]
    #print reviews["stars"]["32"]
    #print reviews["review_id"]["32"]
    #print reviews["date"]["32"]

    reviewsFile = open('reviews.dat', 'w')
    reviewsFile.seek(0)

    bId = reviews["business_id"]
    text = reviews["text"]
    star = reviews["stars"]
    rId = reviews["review_id"]

    #counter = 0
    for index in reviews["review_id"]:
        if index in bId and index in text and index in star and index in rId:
            line = quote + rId[index].replace('\"','\"\"') + quote +\
                   columnSeparator + quote + bId[index].replace('\"','\"\"') + quote +\
                   columnSeparator + quote + text[index].replace('\"','\"\"') + quote +\
                   columnSeparator + str(star[index])

            reviewsFile.write(line.encode('utf-8'))
            reviewsFile.write('\n')
    #counter += 1
    #if counter > 30000:
    #    break
    reviewsFile.close()

if __name__=="__main__":
    main()
