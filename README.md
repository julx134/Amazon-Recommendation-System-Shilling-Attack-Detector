# Amazon-Recommendation-System

![](roadmap.JPG)

## Links
Please see _*links.txt*_ for links to the dataset used in this repository. <br/>
:link: [Recommendation System](https://colab.research.google.com/drive/19Qat-59Rz7laqR9NSibKeBcxBSBtFptx?usp=sharing) <br/>
:link: [LSTM Shilling Attack Detector](https://colab.research.google.com/drive/1oA1rTGMnUxWPxsm3rWcF8cNecQDPX8yw?usp=sharing) <br/>
:link: [CNN Shilling Attack Detector](https://colab.research.google.com/drive/1E6D4UKCTQL7YVbmplVCWP_BcgSSdCC07?usp=sharing) <br/>
:link: [CNN-LSTM Shilling Attack Detector](https://colab.research.google.com/drive/183Z421C9Tuh52-CHn5HEmmAE9jlmpEb-?usp=sharing)



## Item-Based Collobarative-Filtering Recommendation System (ICBFRS)
Collaborative Filtering (CF) produces recommendations by evaluating the ratings of items by users.<br/>
1) Pre-process datasets to remove incosistencies and type errors
2) Create the user-item matrix
3) Employ a similarity algorithm such as cosine and Pearson to find features/similarities between items
4) Find the top Kth nearest neighbours for an item using weighted averages of items similar to the items the user has rated


## Scikit-learn Recommendation System Library
The name SurPRISE (roughly :) ) stands for Simple Python RecommendatIon System Engine. <br/>
We use the SurPRISE library to quickly build, train and evaluate a simple ICBFRS.
We initially implemented the ICBFRS manually, however, we did not have access to good hardware
resources to train the model and that we did not have a computationally efficient backend to handle all this processing. A _**very small**_ sample of sparse matrix is shown below where the red cells are values that are not zero. For this reason, we also moved our development environment over to Google Collab to take advantage of their hardware resources<br/><br/>
![](sparse_matrix.JPG)
<br/>

## Shilling Attacks
A shilling attack is any form of malicious intent by a user or organization on recommendation systems in order to sway the prediction model to their economic benefit and/or at the economic cost of others. There are multiple types of attacks but they can be classified either into low-level attacks and high-level attacks where high-level attacks require the attacker to know the domian knowledge in depth, whereas low-level attacks do not. <br/>

### LSTM Shilling Attack Dectector
To detect these attacks, we use a Long Short Term Memory network to capture contextual dependencies of users vs. shilling attackers. To do this, we first pre-process the ratings dataset into user-item vectors where each vector represents a user and all of their item ratings (any items not rated will be set to zero). Then we feed these vectors into the model with the following architecture: <br/>
![](lstm_architecture.JPG)
<br/>
Finally, we cluster the predictions using k-means clustering to classify the users as either being an authentic user or a shilling attacker. A sample probability distribution graph of the predictions is shown below: </br>
![](lstm_probability_distribution.JPG)

