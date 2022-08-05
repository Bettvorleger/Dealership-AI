import pandas as pd
import numpy as np
import os
import mlflow
import mlflow.sklearn

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from minio import Minio

def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2

if __name__ == "__main__":

    os.environ['MLFLOW_TRACKING_USERNAME'] = 'group5'
    os.environ['MLFLOW_TRACKING_PASSWORD'] = 'BVT4mSsG4'
    os.environ['MLFLOW_TRACKING_URI'] = 'https://mlflow.sws.informatik.uni-leipzig.de'

    client = Minio(
        "api.storage.sws.informatik.uni-leipzig.de",
        access_key="90iLSEUoCzGrPci8",
        secret_key="6scbjD5fbUSKuD1VULwNeAoaOlVAurIu",
    )

    a24_obj = client.get_object("group5", "a24_data/autoscout24-germany-dataset.csv")
    cars = pd.read_csv(a24_obj)

    #########################
    ##### Preprocessing #####
    #########################

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

    #########################
    ### Linear Regression ###
    #########################

    #regr = LinearRegression()
    #regr.fit(X_train, Y_train)

    #########################
    ### Ridge Regression ####
    #########################

    #regr = Ridge(alpha=0.0)
    #regr.fit(X_train, Y_train)

    #########################
    ### Lasso Regression ####
    #########################

    regr = Lasso(alpha=0.0)
    regr.fit(X_train, Y_train)

    predicted = regr.predict(X_test)

    # our experiment name in mlflow
    experiment = mlflow.get_experiment_by_name('group5-linear-regression')

    client = mlflow.tracking.MlflowClient()
    
    run = client.create_run(experiment.experiment_id)

    with mlflow.start_run(run_id = run.info.run_id, experiment_id=experiment.experiment_id):

        (rmse, mae, r2) = eval_metrics(Y_test, predicted)

        print("Linear model:")
        print("  RMSE: %s" % rmse)
        print("  MAE: %s" % mae)
        print("  R2: %s" % r2)

        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        mlflow.log_metric("mae", mae)

        mlflow.sklearn.log_model(regr, 'linearmodel')

        mlflow.end_run()