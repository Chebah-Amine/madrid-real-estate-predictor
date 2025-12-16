from abc import ABC, abstractmethod
class Predictor(ABC):
    @abstractmethod
    def predict(self, input_data):
        pass

    def train(self, x_train, y_train, x_test, y_test):
        pass

    def save(self):
        pass

    def load(self):
        pass