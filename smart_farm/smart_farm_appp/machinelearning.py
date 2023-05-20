import pandas as pd
import numpy as np
from sklearn import linear_model

class mlirigasi:
    def __init__(self):
        self.reg = linear_model.LinearRegression()
        df = pd.DataFrame({'kelembaban': [10, 30, 50, 70, 90],
                        'ph': [1, 3, 7, 9, 12],
                        'suhu': [50, 40, 27, 10, -10],
                        'sprinkler': [30, 25, 20, 10, 1]})
        self.reg.fit(df[['kelembaban', 'ph', 'suhu']], df.sprinkler)

    
    def hitungml(self, kelembaban, ph, suhu):
        return self.reg.predict([[kelembaban, ph, suhu]])[0]
