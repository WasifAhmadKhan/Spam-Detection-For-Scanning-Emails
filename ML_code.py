import os
import pickle

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib


class Classifier:
    score = 0

    def __init__(self, filepath):
        self.vectorizer = TfidfVectorizer(min_df=1, stop_words='english')
        self.mnb = MultinomialNB()
        self.file_path = filepath

    def setup_trainer(self, filepath):
        df = pd.read_csv(filepath, sep='\t', names=['Status', 'Message'])
        df.loc[df["Status"] == 'ham', "Status"] = 1
        df.loc[df["Status"] == 'spam', "Status"] = 0
        df_x = df["Message"]
        df_y = df["Status"]
        return df_x, df_y

    def train(self):
        print('training')
        df_x, df_y = self.setup_trainer(self.file_path)
        x_train, x_test, y_train, y_test = train_test_split(df_x, df_y, test_size=0.2, random_state=4)
        y_train = y_train.astype('int')
        y_test = y_test.astype('int')
        x_train_vec = self.vectorizer.fit_transform(x_train)
        x_test_vec = self.vectorizer.transform(x_test)
        self.mnb.fit(x_train_vec, y_train)
        self.score = self.mnb.score(x_test_vec, y_test)
        return self.score, self.mnb

    def predict_text(self, msg, model=None):

        try:
            if model is None:
                vectorized_msg = self.vectorizer.transform([msg])
                result = self.mnb.predict(vectorized_msg)
            else:

                vectorized_msg = self.vectorizer.transform([msg])
                result = model.predict(vectorized_msg)
            if result[0] == 1:
                return {msg: "not spam"}
            else:
                return {msg: "spam"}
        except Exception as e:
            print(e)

    def save_model(self, model_name, model_obj):
        path = os.path.join('models', f'{model_name}.pkl')
        file = open(path, 'wb')
        pickle.dump(model_obj, file)
        return "saved"

    def load_model(self, model_name):
        path = os.path.join('models', f'{model_name}.pkl')
        file = open(path, 'rb')
        return pickle.load(file)

    def set_model(self, model,vector):
        print('updated model to', model)
        self.mnb = model
        self.vectorizer=vector

    def help(self):
        print('run the functions in following order')
