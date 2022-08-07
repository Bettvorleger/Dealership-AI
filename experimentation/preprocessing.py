import pandas as pd
import numpy as np
import requests

def preprocess_data(cars):

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

    return cars

def get_a24_data(client):
    try:
        a24_obj = client.get_object("group5", "a24_data/autoscout24-germany-dataset.csv")
        cars = pd.read_csv(a24_obj)

    finally:
        a24_obj.close()
        a24_obj.release_conn()

    return cars

def get_scraping_data(client):

    weeks = list(range(1,53))

    cars = pd.DataFrame()

    for week in weeks:
        try:
            path = "scraping_data/week_" + str(week) + "/scraped_car_data.csv"
            
            try:
                scraping_obj = client.get_object("group5", path)
                cars_scraped = pd.read_csv(scraping_obj, sep=';')

            finally:
                scraping_obj.close()
                scraping_obj.release_conn()


            for column in cars_scraped.columns:
                indices_to_be_deleted = cars_scraped.index[cars_scraped[column].isnull()].tolist()
                cars_scraped = cars_scraped.drop(indices_to_be_deleted)

            cars_scraped = cars_scraped.astype({"mileage": "int64", "price": "int64", "year": "int64"})

            cars = pd.concat([cars, cars_scraped], ignore_index=True)

        except Exception as e:
            #print(e)
            pass

    return cars

def get_sold_data():

    url = "http://t5.se4ai.sws.informatik.uni-leipzig.de/fastapi/soldCars"
    
    resp = requests.get(url=url)

    cars = pd.DataFrame()

    for sold_car in resp.json():

        sold_car = pd.DataFrame([sold_car])

        column_mileage = sold_car["mileage"]
        column_price = sold_car["price"]

        sold_car.drop("mileage", axis=1, inplace=True)
        sold_car.insert(0, "mileage", column_mileage)

        sold_car.drop("price", axis=1, inplace=True)
        sold_car.insert(6, "price", column_price)

        sold_car = sold_car.astype({"hp": "float64"})
        sold_car = sold_car.rename(columns={"offer_type": "offerType"})

        cars = pd.concat([cars, sold_car], ignore_index=True)

    return cars


