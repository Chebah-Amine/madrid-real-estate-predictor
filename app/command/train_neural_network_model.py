from sklearn.model_selection import train_test_split
from app.model.neural_network_model import NeuralNetworkModel
from app.command.utils.utils import metrics, load_data, encode_data


def main():
    # Charger et préparer les données
    data = load_data('app/static/dataset/dataset_back_ml.csv')
    x, y = encode_data(data)

    # Diviser les données en ensembles d'entraînement et de test
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)

    input_shape = x_train.shape[1]
    model = NeuralNetworkModel(model_path="app/static/model/trained_neural_network.h5")
    model.build(input_shape)

    # Entraîner le modèle
    model.train(x_train, y_train, x_test, y_test)

    model.save()
    metrics(model, x_test, y_test)


if __name__ == '__main__':
    main()
