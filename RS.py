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


# Read in data
ratings=pd.read_excel('dataset/appliances_subset.xlsx')
uniqueUsers = ratings['userId'].nunique()
uniqueItems = ratings['asin'].nunique()
print(f'The provided amazon dataset has: {uniqueUsers} unique users and {uniqueItems} unique items')

# get metadata for appliances
metadata = []
with gzip.open('dataset/meta_Appliances.json.gz') as f:
    for l in f:
        metadata.append(json.loads(l.strip()))
    
df1 = pd.DataFrame.from_dict(metadata)

df3 = df1.fillna('')
# filter those unformatted rows
df5 = df3[~df3.title.str.contains('getTime')] 
df6 = df5[~df5.tech1.str.contains('\\n')]

#convert list to dataframe
finalDf = pd.DataFrame(df6, columns = ['asin', 'title'])
#finalDf.to_csv('asin_title.csv')
appliance_metadata = finalDf.values.tolist()


# Create user-item matrix
print('creating item-user matrix...')
matrix = ratings.pivot_table(index='asin', columns='userId', values='rating')

# Normalize user-item matrix
print('normalizing matrix...')
matrix_norm = matrix.subtract(matrix.mean(axis=1), axis = 0)
#matrix_norm.to_csv('normalized.csv')

# Item similarity matrix using pearson correlation
print('performing pearson correlation...')
item_similarity = matrix_norm.T.corr(method = 'pearson')
#item_similarity.to_csv('pearson.csv')

def item_based_rec(userId, knn):
    ##dictionary for returning recommended items
    recommended_items = dict()

    #1) get list of unrated appliances of the user
    unratedAppliances = pd.DataFrame(matrix_norm[userId].isna()).reset_index()
    unratedAppliances = unratedAppliances[unratedAppliances[userId]==True]['asin'].values.tolist()
    
    #2) get dataframe of appliances rated by the user
    ratedAppliances = pd.DataFrame((matrix_norm[userId]).dropna(axis = 0, how = 'all').sort_values(ascending=False)).reset_index().rename(columns={userId:'rating'})
    
    #3) Loop through unrated appliances and generate rating for each appliance
    for appliance in unratedAppliances:
        appliance_dict = generateApplianceRating(userId, appliance, knn)
        recommended_items[getApplianceTitle(appliance)] = appliance_dict['predicted_rating']

    print(ratedAppliances)
    return sorted(recommended_items.items(), key=operator.itemgetter(1), reverse=True)[:5]
    #return recommended_items

def generateApplianceRating(userId, pickedAppliance, knn):
    ##dictionary to return df and predicted value
    return_val = dict()

    #1) get dataframe of all the appliances that the user has rated
    ratedAppliances = pd.DataFrame(matrix_norm[userId].dropna(axis=0, how='all').sort_values(ascending=False).reset_index().rename(columns={userId:'rating'}))
    
    #2) get dataframe of the similarity vector of picked appliances
    pickedAppliance_similarity_vector = item_similarity[[pickedAppliance]].reset_index().rename(columns = {pickedAppliance : 'similarity_score'})
    
    #3 sort similarity vector in descending order and pick top kth neighbours. 
    # Then join vector with ratedAppliances so we get user rating and similarity score (if applicable)
    recommended_df = pd.merge(left = ratedAppliances, right = pickedAppliance_similarity_vector, on = 'asin', how = 'inner').sort_values('similarity_score', ascending=False)

    #calculate weighted average of kth neighbours
    #col_mean = recommended_df['similarity_score'].fillna(0).mean()
    #print(f'{pickedAppliance} col mean is : {col_mean}')
    recommended_df['similarity_score'] = recommended_df['similarity_score'].fillna(1)
    if(len(recommended_df.index) < knn):
        new_knn = len(recommended_df.index)
        recommended_df = recommended_df[:new_knn]
        predicted_rating = round(np.average(recommended_df['rating'], weights = recommended_df['similarity_score'] ), 2)
    else:
        predicted_rating = round(np.average(recommended_df['rating'], weights = recommended_df['similarity_score'] ), 2)
    
    return_val['df'] = recommended_df
    return_val['predicted_rating'] = predicted_rating
    return return_val

def getApplianceTitle(asin): 
    try:
        return appliance_metadata[appliance_metadata.index(asin)]
    except:
        return asin   

test = item_based_rec("A3NHUQ33CFH3VM",5)
print(test)
#test = generateApplianceRating("A3NHUQ33CFH3VM", "B0001Q46B2", 5)
#print(test)