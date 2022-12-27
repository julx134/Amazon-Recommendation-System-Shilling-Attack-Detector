###### mport Python Libraries
# Data processing
import pandas as pd
import json
import gzip
import numpy as np
import operator
import scipy.stats
# Visualization
#import seaborn as sns
# Similarity
from sklearn.metrics.pairwise import cosine_similarity
import os
from surprise import BaselineOnly, Dataset, Reader
from surprise.model_selection import cross_validate


# path to dataset file
file_path = os.path.expanduser("~/Desktop/Capstone_RS/dataset/appliances_subset.csv")

# As we're loading a custom dataset, we need to define a reader. In the
# movielens-100k dataset, each line has the following format:
# 'user item rating timestamp', separated by '\t' characters.
reader = Reader(line_format="user item rating timestamp", sep="\t")

#convert to Dataset object
data = Dataset.load_from_file(file_path, reader=reader)

#convert to Trainset object to be used for testing
#More info at: https://surprise.readthedocs.io/en/stable/trainset.html#surprise.Trainset.build_testset
trainset = data.build_testset()

#arguments for algorithm
sim_options = {
    "name": "cosine",
    "user_based": False,  # compute  similarities between items
}

#choosen algorithm: k-NN 
#there are also multiple options for k-NN based algos: https://surprise.readthedocs.io/en/stable/knn_inspired.html#pred-package-knn-inpired
algo = KNNBasic(sim_options=sim_options)

#fit algorithm to training set
algo.fit(trainset)


#Once fitted, we can call functions from the surprise library to get outputs that we need
#link: https://surprise.readthedocs.io/en/stable/algobase.html

#returns similarity matrix
algo.compute_similarities()

#returns Prediction object
algo.test(trainset)

#return predriction for given user and item
algo.predict(userID, ASIN)