import pandas as pd
import numpy as np
import os
import mlflow
import mlflow.sklearn

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso

from sklearn.linear_model import ElasticNetCV
from sklearn.model_selection import RepeatedKFold

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from preprocessing import get_a24_data, get_scraping_data, get_sold_data, preprocess_data

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

    if os.environ.get("MLFLOW_RUN_NAME") == None:
        run_name = "local"
    else:
        run_name = os.environ.get("MLFLOW_RUN_NAME")

    client = Minio(
        "api.storage.sws.informatik.uni-leipzig.de",
        access_key="90iLSEUoCzGrPci8",
        secret_key="6scbjD5fbUSKuD1VULwNeAoaOlVAurIu",
    )

    cars = get_a24_data(client)
    #print(cars.size)
    #print(cars)
    #print(cars.dtypes)

    cars_scraped = get_scraping_data(client)
    #print(cars_scraped.size)
    #print(cars_scraped)
    #print(cars_scraped.dtypes)

    cars_sold = get_sold_data()
    #print(cars_sold.size)
    #print(cars_sold)
    #print(cars_sold.dtypes)

    ### concat all data ###

    #cars = pd.concat([cars, cars_scraped, cars_sold], ignore_index=True)
    #print(cars.size)
    #print(cars)
    #print(cars.dtypes)
    
    #########################
    ##### Preprocessing #####
    #########################

    cars = preprocess_data(cars)

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
    #run_name = run_name + "_Linear_a24_data"

    #########################
    ### Lasso Regression ####
    #########################

    regr = Lasso(alpha=0.0, max_iter=100000)
    regr.fit(X_train, Y_train)
    run_name = run_name + "_Lasso_a24_data"

    #########################
    ##### ElasticNetCV ######
    #########################

    #alphas = [1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 0.0, 1.0, 10.0, 100.0]
    #l1_ratios = np.arange(0, 1, 0.01)

    #cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
    #regr = ElasticNetCV(alphas=alphas, l1_ratio=l1_ratios, max_iter=100000, cv=cv, n_jobs=-1).fit(X_train, Y_train)

    #run_name = run_name + "_Elastic_all_data"

    # predict on X_test
    predicted = regr.predict(X_test)

    # our experiment name in mlflow
    experiment = mlflow.get_experiment_by_name('group5-linear-regression')

    client = mlflow.tracking.MlflowClient()
    
    run = client.create_run(experiment.experiment_id, tags={"name":run_name})

    with mlflow.start_run(run_id = run.info.run_id):

        (rmse, mae, r2) = eval_metrics(Y_test, predicted)

        print("Linear model:")
        print("  RMSE: %s" % rmse)
        print("  MAE: %s" % mae)
        print("  R2: %s" % r2)

        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        mlflow.log_metric("mae", mae)

        #print('alpha: %f' % regr.alpha_)
        #print('l1_ratio_: %f' % regr.l1_ratio_)

        #mlflow.log_param("alpha", regr.alpha_)
        #mlflow.log_param("l1_ratio", regr.l1_ratio_)

        mlflow.sklearn.log_model(regr, 'linearmodel')

        mlflow.end_run()