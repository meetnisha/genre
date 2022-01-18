# genre
Classification music genre

# Create a virtual environment
python3 -m venv music
source music/bin/activate

# To use as docker, clone repo and run
docker-compose up -d --build

Or 

docker-compose -f docker-compose.yml up -d --build

# To check log files
docker logs -f core-api-container

# Screenshots

Home - homepage.png

Prediction output - afterprediction.png

Search Page - searchpage.png

# OpenSpec API
http://localhost:8000/docs

## Conclusion of ML analysis
File: /app/analysis/EDA_ML.ipynb

One shouldnot get 100% accuracy from your training dataset. This means my model is overfitting.

XGBoost Test Accuracy - 65.71. 
1. I tried to find better hyper paramaters like n_estimators, reg_lambda but the space was too large.
2. I applied dimensionalty reducing technique like PCA but the accuracy got worse.
3. It consumed lots of time and hence I decided to move to Deep Learning.

### Check EDA_DL file for further analysis

As I need to decrease the complexity by removing features, I used recursive feature elimination but it took almost 24 hours to run on my machine. 
Hence the features extracted in my ML analysis are used to build a deep learning model where I wanted to use title and tags feature as well.

## Conclusion of DL Analysis
File: /app/analysis/EDA_DL.ipynb

1. Cleaned data, removed all null values
2. Dropped highly co-related features
3. Used recursive feature elimination(RFECV) in XGBClassifier in ML analysis, I eliminated those features for DL model as well.
4. Trid few optimizers like sgd, rmsprop and adam. Model performed better with adam.
5. Base line model overfitted.
6. Apply few techniques like regularization, drop outs and early stopping 
7. Drop puts performed better.
8. XGBoost Test Accuracy - 65.71 %
    a. I tried to find better hyper paramaters like n_estimators, reg_lambda but the space was too large.
    b. It consumed lots of time and hence I decided to move to Deep Learning.
9. Baseline DL model - 63.13%
10. Best performing model - Dropout model - Test Accuracy - 70.89%
