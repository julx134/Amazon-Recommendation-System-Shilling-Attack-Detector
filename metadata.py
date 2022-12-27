# Read in metadata
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

#merge data and metadata
df = pd.merge(ratings, finalDf, on='asin', how='inner')
agg_rating = df.groupby('title').agg(mean_rating = ('rating', 'mean'), number_of_ratings = ('rating','count')).reset_index()