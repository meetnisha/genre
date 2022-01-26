# Objective
Genre Classification of Million Song Dataset

# Create a virtual environment
python3 -m venv music

source music/bin/activate

# Steps to run the project locally
Make sure docker is setup in your system. Then follow these steps to install the project:

1. clone the project by using: `git clone git@github.com:meetnisha/genre.git`
Run these commands in the project's folder:

2. `git submodule update --init --recursive`

3. run `./run_local.sh` in root folder of the project

Alternatively, clone repo and run

docker-compose up -d --build

Or 

docker-compose -f docker-compose.yaml up -d --build

## To check log files
docker logs -f core-api-container

# Application 
## Report
Please check Report.docx for details about this application

## Screenshots

1. Home - homepage.png
2. Prediction output - afterprediction.png
3. Search Page - searchpage.png

## Home Page
http://localhost:8000/

<<<<<<< HEAD
## Prediction Output file
=======
# Output file
>>>>>>> d5e21a0c4ae60839faf8f186f0a7f3dbdb3e2813
The test output file is saved in this folder:

/data/test_prediction.csv

## OpenSpec API
http://localhost:8000/docs

# Conclusion of ML analysis
File: /app/analysis/EDA_ML.ipynb

One shouldnot get 100% accuracy from your training dataset. This means my model is overfitting.

XGBoost Test Accuracy - 65.71. 
1. I tried to find better hyper paramaters like n_estimators, reg_lambda but the space was too large.
2. I applied dimensionalty reducing technique like PCA but the accuracy got worse.
3. It consumed lots of time and hence I decided to move to Deep Learning.

### Check EDA_DL file for further analysis

As I need to decrease the complexity by removing features, I used recursive feature elimination but it took almost 24 hours to run on my machine. 
Hence the features extracted in my ML analysis are used to build a deep learning model where I wanted to use title and tags feature as well.

# Conclusion of DL Analysis
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