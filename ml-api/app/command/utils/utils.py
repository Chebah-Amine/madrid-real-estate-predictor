from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, make_scorer
import numpy as np
import pandas as pd
from app.preprocessing.data_processor import DataPreprocessor

def load_data(filepath):
    data = pd.read_csv(filepath, index_col='id')
    data.drop(columns=['Unnamed: 0'], inplace=True)
    return data
def encode_data(data):
    preprocessor = DataPreprocessor(save_path="app/static/encoder/column_transformer.pkl")
    preprocessor.build()
    x, y = preprocessor.fit_transform(data)
    return x, y

def metrics(model, x_test, y_test):
    y_pred_log = model.predict(x_test)
    y_pred = np.expm1(y_pred_log)
    y_true = np.expm1(y_test)
    mse = mean_squared_error(y_true, y_pred)
    print(f'MSE: {mse}')
    rmse = np.sqrt(mse)
    print(f'RMSE: {rmse}')
    mae = mean_absolute_error(y_true, y_pred)
    print(f'MAE: {mae}')
    # Calcul du coefficient de détermination R²
    r2 = r2_score(y_true, y_pred)
    print(f'Coefficient de détermination R²: {r2:.2%}')