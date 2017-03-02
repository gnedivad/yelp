
# coding: utf-8

# In[1]:

import os

import pandas as pd


# In[2]:

BUSINESS = 'yelp_academic_dataset_business.json'
CHECKIN = 'yelp_academic_dataset_checkin.json'
REVIEW = 'yelp_academic_dataset_review.json'
TIP = 'yelp_academic_dataset_tip.json'
USER = 'yelp_academic_dataset_user.json'


# In[ ]:

for inp in [BUSINESS,CHECKIN,TIP,REVIEW]:
    data_json_str = '['
    with open(os.path.join('data',inp)) as fp:
        for line in fp:
            data_json_str += line + ','
    data_json_str += ']'
    # now, load it into pandas
    df = pd.read_json(data_json_str)
    print df.columns
    raise
    types = df.apply(lambda x: pd.lib.infer_dtype(x.values))
    if inp == BUSINESS:
        df = df[df['categories'].apply(lambda x: (True if 'Restaurants' in x else False) if type(x) is list else False)]
        uni_id = list(df.business_id)
    else:
        df = df[df.business_id.isin(uni_id)]

    fl, ext = os.path.splitext(inp)
    out_name = os.path.join('data',fl.split('_')[-1] + '.tsv')
    out_name2 = os.path.join('data',fl.split('_')[-1] + '.json')
    df.to_csv(out_name,sep='\t',encoding='utf-8')
    df.to_json(out_name2)


# In[54]:



# In[ ]:



