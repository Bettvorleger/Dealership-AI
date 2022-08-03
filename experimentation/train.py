import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import os
import mlflow.sklearn

os.environ['MLFLOW_TRACKING_USERNAME'] = 'group5'
os.environ['MLFLOW_TRACKING_PASSWORD'] = 'BVT4mSsG4'
os.environ['MLFLOW_TRACKING_URI'] = 'https://mlflow.sws.informatik.uni-leipzig.de'

# our experiment name in mlflow
mlflow.set_experiment('group5-linear-regression')

path_to_data = "../data/autoscout24-germany-dataset.csv"
cars = pd.read_csv(path_to_data)

# unsinnige Einträge für "Marke" löschen
indices_to_be_deleted = cars.index[
    cars['make'].isin(['Trucks-Lkw', 'Caravans-Wohnm', 'Trailer-Anhänger', 'Others', 'Piaggio'])].tolist()
cars = cars.drop(indices_to_be_deleted)

# Falsch benannte Marken korrigieren
# Alfa -> Alfa Romeo, Land -> Land Rover, Aston -> Aston Martin
cars['make'] = cars['make'].replace(['Alfa', 'Land', 'Aston'], ['Alfa Romeo', 'Land Rover', 'Aston Martin'])

# Falsch benannte Modelle korrigieren
cars.loc[cars['make'].isin(['Alfa Romeo', 'Land Rover']), 'model'] = cars.loc[cars['make'].isin(
    ['Alfa Romeo', 'Land Rover']), 'model'].str[6:]
cars.loc[cars['make'] == 'Aston Martin', 'model'] = cars.loc[cars['make'] == 'Aston Martin', 'model'].str[7:]

# Unsinnige Werte für 'fuel' löschen
indices_to_be_deleted = cars.index[cars['fuel'].isin(['-/- (Fuel)', 'Others'])].tolist()
cars = cars.drop(indices_to_be_deleted)

# Unsinnige Werte für 'hp' löschen
indices_to_be_deleted = cars.index[cars['hp'] == 1.0].tolist()
cars = cars.drop(indices_to_be_deleted)

# Leere Werte löschen
indices_to_be_deleted = cars.index[cars['model'].isnull()].tolist()
cars = cars.drop(indices_to_be_deleted)
indices_to_be_deleted = cars.index[cars['gear'].isnull()].tolist()
cars = cars.drop(indices_to_be_deleted)
indices_to_be_deleted = cars.index[cars['hp'].isnull()].tolist()
cars = cars.drop(indices_to_be_deleted)

# Variables for regression, X = matrix of regressors (all except price), Y contains regressand: price
X = cars.drop('price', axis=1)
Y = cars['price']

# Transform non-numeric attributes to dummy variables for regression
X = pd.get_dummies(data=X, drop_first=True)

# Split the data
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=.20, random_state=40)


def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2


with mlflow.start_run():
    regr = LinearRegression()
    regr.fit(X_train, Y_train)
    predicted = regr.predict(X_test)
    (rmse, mae, r2) = eval_metrics(Y_test, predicted)
    mlflow.log_metric("rmse", rmse)
    mlflow.log_metric("r2", r2)
    mlflow.log_metric("mae", mae)
    mlflow.sklearn.log_model(regr, 'linearmodel')
