from surprise import Dataset, SVD
from surprise.model_selection import cross_validate
from surprise import KNNBasic


# Load the movielens-100k dataset (download it if needed),
data = Dataset.load_builtin("ml-100k")

# We'll use the item-based collaborative filtering algorithm
sim_options = {
    "name": "cosine",
    "user_based": False,  # compute  similarities between items
}
algo = KNNBasic(sim_options=sim_options)

# Run 5-fold cross-validation and print results
cross_validate(algo, data, measures=["RMSE", "MAE"], cv=5, verbose=True)