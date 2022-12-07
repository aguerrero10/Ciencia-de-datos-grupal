from joblib import load, dump
from sklearn.metrics import precision_score, recall_score, f1_score
import glob


class RetrainModel:

    def __init__(self):
        path = 'C:/Descargas/Compartido/Estudio/Andes - Maestría/Semestre 5/Ciencia de datos aplicada/Talleres/Taller 4/API/models/'
        
        lista = glob.glob(path + '*.joblib')
        lista.sort(reverse=True)
        file = lista[0][2:]

        self.archivo = file
        self.model_original = load(file)

    def make_retrain(self, data):

        X = data.drop(columns='Churn')
        Y = data['Churn'].replace({'No': 0, 'Yes': 1})

        pred_original = self.model_original.predict(X)

        result1_original = precision_score(Y, pred_original)
        result2_original = recall_score(Y, pred_original)
        result3_original = f1_score(Y, pred_original)

        self.model_original.fit(X, Y)

        pred_retrain = self.model_original.predict(X)

        result1_retrain = precision_score(Y, pred_retrain)
        result2_retrain = recall_score(Y, pred_retrain)
        result3_retrain = f1_score(Y, pred_retrain)

        result_original = {"Precisión": result1_original, "Recall":result2_original, "F1 Score": result3_original}
        result_retrain =  {"Precisión": result1_retrain, "Recall": result2_retrain, "F1 Score": result3_retrain}

        return result_original, result_retrain

    def save_model(self):
        archivo = self.archivo
        num = archivo[-8]
        new_num = int(num) + 1
        new_name = archivo[:-8] + str(new_num) + ".joblib"
        dump(self.model_original, new_name)