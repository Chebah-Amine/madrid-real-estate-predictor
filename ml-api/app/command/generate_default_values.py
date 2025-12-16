from app.command.utils.utils import load_data
from app.preprocessing.data_default_values import DefaultValues


def main():
    data = load_data('app/static/dataset/dataset_back_ml.csv')
    defaultValues = DefaultValues(data, 'app/static/dataset/default_values.json')
    defaultValues.calculate_defaults()
    defaultValues.save()

if __name__ == '__main__':
    main()