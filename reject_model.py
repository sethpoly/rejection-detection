import numpy
import pandas as pd



class Classifier:
    def __init__(self):
        self.df = pd.read_csv(self.get_csv())




    # Retrieve most recent rejection data set from sheets API
    def get_csv(self):
        return 0