# The Movies Dataset Recommender System 
[Dataset on kaggle](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset)

## Contents
### Data understanding and EDA
* Histogram
* Bar chart
* Data queries

This part is done on **Data Preparation and EDA** notebook and a clean dataset is saved for the following tasks.

### Data preprocessing 
* Missing values
* Duplicated values
* Encoding (TF IDF)
  
### Modeling
Our model has two inputs, titles of movies and ratings.
The main idea is to use cosine similarity to calculate similarity matrix. After that, for each movie we get top 5 movies from similarity matrix and multiply it to movie's rating and continue the process for all movies.
Let's say user sends us 3 movies with 3 ratings. For first movie we get 5 most closest movies and multiply similarity matrix scores to its rating. After doing this process for all movies we have 15 movies with 15 weighted scores.
At the end we sort the scores and show top 5 movies.


### Deployment
* Streamlit app on hugging face
######
[Model on hugging face](https://huggingface.co/spaces/MehrabK/RecommenderSystem)

