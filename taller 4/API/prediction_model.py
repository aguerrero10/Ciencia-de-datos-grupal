from joblib import load
import xgboost
from xgboost import XGBClassifier
import glob

class PredictionModel:

    def __init__(self):
        #path = 'C:/Descargas/Compartido/Estudio/Andes - Maestría/Semestre 5/Ciencia de datos aplicada/Talleres/Taller 4/API/'
        #self.model = load(path + "models/churn-v1.1.joblib")
        #self.model = load(path + "models/churn-v2.0.joblib")
        path = 'C:/Descargas/Compartido/Estudio/Andes - Maestría/Semestre 5/Ciencia de datos aplicada/Talleres/Taller 4/API/models/'
        
        lista = glob.glob(path + '*.joblib')
        lista.sort(reverse=True)
        file = lista[0][2:]

        self.model = load(file)

    def make_predictions(self, data):
        result = self.model.predict(data)
        return result
