import string, numpy
import pandas as pd
import service_account as acc
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.model_selection import cross_val_score


class Classifier:
    def __init__(self):
        self.df = self.get_csv()
        self.x_train, self.x_test, self.y_train, self.y_test = None


    # Retrieve most recent rejection data set from sheets API
    def get_csv(self):
        data_sheet = acc.Spreadsheet('RejectionData').sheet
        rows = data_sheet.get_all_values()
        return pd.DataFrame.from_records(rows)

    # Removes punctuation, digits, HTML, from EMAIL column in data set
    # df[0] is EMAIL, df[1] is STATUS
    def clean_data(self):
        try:
            self.df[0] = self.df[0].apply(lambda x: x.lower())
            self.df[0] = self.df[0].apply(lambda x: x.translate(str.maketrans('', '', string.punctuation)))
            self.df[0] = self.df[0].apply(lambda x: x.translate(str.maketrans('', '', '1234567890')))
            self.df[0] = self.df[0].apply(lambda x: x.translate(str.maketrans('', '', '\n')))
            print('Successfully cleaned data.')
        except AttributeError as e:
            print(f'Whoops: {repr(e)}')

    def fit(self):
        # pull data into vectors to create collection of text/tokens
        vectorizer = CountVectorizer()
        x = vectorizer.fit_transform(self.df[0])
        encoder = LabelEncoder()
        y = encoder.fit_transform(self.df[1])

        # split into train and test sets
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(x, y, test_size=0.2)

    def print_data(self):
        print(self.df.tail)


model = Classifier()
model.clean_data()
model.fit()


