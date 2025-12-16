import pandas as pd
import joblib
import numpy as np

MODEL_PATH = 'app/static/model/trained_neural_network.h5'
ENCODER_PATH = 'app/static/encoder/column_transformer.pkl'
DEFAULTS_PATH = 'app/static/dataset/default_values.json'

class PredictPriceService:
    def __init__(self, input_house):
        self.input = input_house
        self.model = joblib.load(MODEL_PATH)  # Préchargement du modèle
        self.encoder = joblib.load(ENCODER_PATH)  # Préchargement de l'encodeur
        self.defaults = pd.read_json(DEFAULTS_PATH, typ='series', convert_dates=False)  # Préchargement des valeurs par défaut

    def predict_price(self):
        # Remplir les valeurs manquantes avec les valeurs par défaut
        for key, default_value in self.defaults.items():
            if key not in self.input or self.input[key] is None:
                self.input[key] = default_value

        df = pd.DataFrame([self.input])
        encoded_df = self.encoder.transform(df)  # Utiliser transform() et non fit_transform()
        prediction = self.model.predict(encoded_df)[0][0]

        return float(np.expm1(prediction))
