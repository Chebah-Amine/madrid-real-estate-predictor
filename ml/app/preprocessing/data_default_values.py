import pandas as pd
import joblib
from sklearn.impute import SimpleImputer


class DefaultValues:
    def __init__(self, data, file_path):
        self.data = data.drop(columns=['buy_price'])
        self.file_path = file_path
        self.defaultValues = {}

    def calculate_defaults(self):
        defaults = {}
        for column in self.data.columns:
            if self.data[column].dtype == 'bool':
                self.data[column] = self.data[column].astype(int)
                imputer = SimpleImputer(strategy='most_frequent')
            elif self.data[column].dtype in ['int64', 'float64']:
                imputer = SimpleImputer(strategy='median')
            else:
                imputer = SimpleImputer(strategy='most_frequent')

            imputed_value = imputer.fit_transform(self.data[[column]])[0][0]
            defaults[column] = imputed_value

        self.defaultValues = defaults

    def get_default_by_column(self, column_name):
        return self.defaultValues.get(column_name, None)

    def get_default(self):
        return self.defaultValues

    def save(self):
        # Sauvegarder les valeurs par défaut dans un fichier JSON
        df = pd.DataFrame([self.defaultValues])
        df.to_json(self.file_path, orient='records', lines=True)
        print(f"Default values saved to {self.file_path}")

    def load(self):
        if self.file_path:
            self.defaultValues = joblib.load(self.file_path)
            print(f"Default values loaded from {self.file_path}")
        else:
            print("No file path provided.")
            return None