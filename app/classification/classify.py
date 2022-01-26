
import pickle
import numpy as np
from nltk.corpus import stopwords
from keras.preprocessing.text import Tokenizer
from typing import Tuple

def preprocessing(df: object, sc: object) -> Tuple[object, object]:
    """[summary]
    Preprocess the test data, extract the features for classification
    Args:
        df_test (object): test file
        sc (object): StandardScalar object
    Returns:
        Tuple[object, object]: extracted features, test dataframe
    """
    df = df.dropna()
    df = df.reset_index(drop=True)

    #features to drop based on high correlation
    corr_to_drop = ['vect_43', 'vect_44', 'vect_45', 'vect_46', 'vect_47', 'vect_48', 'vect_49', \
    'vect_50', 'vect_51', 'vect_52', 'vect_53', 'vect_57', 'vect_75', 'vect_76', 'vect_77', 'vect_78', \
    'vect_79', 'vect_80', 'vect_81', 'vect_82', 'vect_83', 'vect_84', 'vect_86', 'vect_95', 'vect_98', \
    'vect_103', 'vect_107', 'vect_108', 'vect_109', 'vect_110', 'vect_111', 'vect_112', 'vect_113', \
    'vect_114', 'vect_115', 'vect_121', 'vect_124', 'vect_127', 'vect_130', 'vect_133', 'vect_136', \
    'vect_137', 'vect_138', 'vect_139', 'vect_140', 'vect_141', 'vect_142', 'vect_143', 'vect_144', \
    'vect_145', 'vect_146', 'vect_148']

    df_test = df.drop(df[corr_to_drop], axis=1)

    #features to drop based on recursive feature elimination on xgboost model
    features_drop_array = ['trackID', 'time_signature', 'key', 'mode', 'vect_12', 'vect_22', 'vect_25', \
    'vect_26', 'vect_33', 'vect_40', 'vect_43', 'vect_49', 'vect_51', 'vect_52', 'vect_56', 'vect_64', \
    'vect_66', 'vect_69', 'vect_70', 'vect_71', 'vect_80', 'vect_82', 'vect_83', 'vect_84', 'vect_87', \
    'vect_89', 'vect_91', 'vect_97', 'vect_98', 'vect_100', 'vect_111', 'vect_113', 'vect_115', \
    'vect_116', 'vect_119', 'vect_123', 'vect_127', 'vect_130', 'vect_144', 'vect_145']

    # final features to drop
    rem_feats_to_drop = list(set(features_drop_array).difference(corr_to_drop))
    df_test = df_test.drop(df_test[rem_feats_to_drop], axis=1)
    
    df_test.title = df_test.title.apply(remove_stopwords)
    df_test.tags = df_test.tags.apply(remove_stopwords)
    df_test = tokenize(df_test)
    
    X_test = sc.fit_transform(np.array(df_test.iloc[:, :], dtype=float))
    
    return X_test, df

def classify_genres(df: object, current: object, loaded_model: object, labels_json_file: object, sc: object, folder: str) -> object:
    """[summary]
    Preprocess and classify the test file
    Args:
        df (object): original uploaded test file
        current (object): current date time
        loaded_model (object): Model loaded into object
        labels_json_file (object): File containing the mappings of the label numbers and genre names
        sc (object): StandardScalar object
        folder (str): folder path of saved models

    Returns:
        object: return the classification data
    """

    X_test, df_test = preprocessing(df, sc)

    y_pred_new = loaded_model.predict(X_test)
    classes = np.argmax(y_pred_new, axis = 1)

    new_genres = dict(zip(labels_json_file.values(),labels_json_file.keys()))
    labels = [new_genres[k] for k in classes]

    df_test['genre'] = labels
    df_test['created'] = current

    df_test_new = df_test[['trackID','title', 'genre', 'created']]
    #Saving the file
    df_test_new.to_csv(folder + '/output/test_prediction.csv')
    return df_test_new, new_genres

def remove_stopwords(input_text):
    '''
    Function to remove English stopwords from a Pandas Series.
    
    Parameters:
        input_text : text to clean
    Output:
        cleaned Pandas Series 
    '''
    stopwords_list = stopwords.words('english')
    # Some words which might indicate a certain sentiment are kept via a whitelist
    whitelist = ["n't", "not", "no"]
    words = input_text.split() 
    clean_words = [word for word in words if (word not in stopwords_list or word in whitelist) and len(word) > 1] 
    return " ".join(clean_words) 

    
def tokenize(df_test: object) -> object:
    """[summary]
    Function to tokenize the title and tags
    Args:
        df_test (object): test dataframe 

    Returns:
        object: modified dataframe
    """
    NB_WORDS = 10000  # Parameter indicating the number of words we'll put in the dictionary
    tk = Tokenizer(num_words=NB_WORDS,
                filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{"}~\t\n',
                lower=True,
                char_level=False,
                split=' ')
    tk.fit_on_texts(df_test.title)
    df_test.title = tk.texts_to_matrix(df_test.title, mode='binary')
    tk.fit_on_texts(df_test.tags)
    df_test.tags = tk.texts_to_matrix(df_test.tags, mode='binary')
    return df_test