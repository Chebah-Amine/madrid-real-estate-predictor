import joblib
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder


class DataPreprocessor:
    def __init__(self, save_path):
        self.preprocessor = None
        self.numeric_features = ['sq_mt_built', 'n_rooms', 'n_bathrooms', 'rent_price',
                                'buy_price_by_area', 'latitude', 'longitude']
        self.categorical_features = ['floor', 'house_type_id', 'energy_certificate',
                                    'is_orientation_north', 'is_orientation_west', 'is_orientation_south',
                                     'is_orientation_east', 'subtitle']
        self.save_path = save_path

    def build(self):
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), self.numeric_features),
                ('cat', OneHotEncoder(), self.categorical_features)
            ],
            remainder='passthrough'
        )

    def fit_transform(self, df):
        x = self.preprocessor.fit_transform(df.drop('buy_price', axis=1))
        y = np.log1p(df['buy_price'].values)
        if self.save_path:
            self.save()
        return x, y

    def save(self):
        joblib.dump(self.preprocessor, self.save_path)
        print(f"Preprocessor saved to {self.save_path}")

    def load(self):
        if self.save_path:
            self.preprocessor = joblib.load(self.save_path)
            print(f"Preprocessor loaded from {self.save_path}")
        else:
            print("No save path provided.")
            return None
