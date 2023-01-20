from surprise import Dataset, Reader, KNNBasic
from surprise.model_selection import cross_validate
from surprise import KNNBasic
import os
import csv
import pandas as pd


# path to dataset file
#file_path = os.path.expanduser("~/Desktop/Capstone_RS/dataset/Appliances_subset_surprise.csv")
file_path = os.path.expanduser("~\Documents\GitHub\Amazon-Recommendation-System\dataset\Appliances_subset_surprise.csv")

#convert csv to dictionary
rating_dict = {'user_id':[], 'item_id':[], 'rating':[]}
with open(file_path, 'r') as dataset:
    for line in csv.reader(dataset):
        rating_dict['user_id'].append(line[0])
        rating_dict['item_id'].append(line[2])
        rating_dict['rating'].append(line[4])

#convert dictionary to dataframe
rating_df = pd.DataFrame.from_dict(rating_dict)


#print(rating_df.value_counts())

#group duplicate values into one rating
rating_df = rating_df.groupby(['user_id', 'item_id']).agg({'rating':'mean'}).reset_index()

#define surprise reader object
reader = Reader(rating_scale=(1,5))

#convert dataframe into surprise dataset object
data = Dataset.load_from_df(rating_df[['user_id', 'item_id', 'rating']], reader)

# We'll use the item-based collaborative filtering algorithm
sim_options = {
    "name": "cosine",
    "user_based": False,  # compute  similarities between items
}
#define IBCFRS
algo = KNNBasic(sim_options=sim_options)

# Run 5-fold cross-validation and print results
cross_validate(algo, data, measures=["RMSE", "MAE"], cv=5, verbose=True)