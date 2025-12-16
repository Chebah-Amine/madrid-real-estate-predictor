import os
from .predictor import Predictor
import tensorflow as tf
import joblib

class NeuralNetworkModel(Predictor):
    def __init__(self, model_path):
        self.model_path = model_path
        self.model = None

    def build(self, input_shape):
        self.model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(input_shape,)),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(64, activation='sigmoid'),
            tf.keras.layers.Dense(1)  # Sortie
        ])

        optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
        self.model.compile(optimizer=optimizer, loss="mean_squared_error")

    def predict(self, input_data):
        return self.model.predict(input_data)

    def train(self, x_train, y_train, x_test, y_test):
        self.model.fit(x_train, y_train, epochs=10, batch_size=16, validation_data=(x_test, y_test))

    def save(self):
        if self.model_path:
            joblib.dump(self.model, self.model_path)
            print(f"Model saved to {self.model_path}")
        else:
            print("Model path not provided. Model not saved.")

    def load(self):
        if self.model_path and os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            print(f"Model loaded from {self.model_path}")
        else:
            print("Model path not provided or model does not exist.")
