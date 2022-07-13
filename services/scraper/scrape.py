from bs4 import BeautifulSoup, SoupStrainer
import requests
from time import sleep
import json
from datetime import datetime
import os
import pandas as pd
from minio import Minio

# set folders locally and on S3
data_folder = "data/"


s3_folder = "scraping_data/"
path_visited_urls = data_folder+"visited_urls.json"

# global urls list
visited_urls = []


def createStructure():
    # create folder for data !!REPLACED BY S3 STORAGE OR POSTGRES DB
    if not os.path.isdir(data_folder):
        os.mkdir(data_folder)
        print(data_folder, "erstellt.")
    else:
        print(data_folder, "existiert bereits")

    # delete visited json file if existent
    if os.path.isfile(path_visited_urls):
        os.remove(path_visited_urls)

    # delete csv file if existent
    if os.path.isfile(data_folder+"scraped_car_data.csv"):
        os.remove(data_folder+"scraped_car_data.csv")


def createList():

    global visited_urls

    # create minio client
    client = Minio(
        "api.storage.sws.informatik.uni-leipzig.de",
        access_key="90iLSEUoCzGrPci8",
        secret_key="6scbjD5fbUSKuD1VULwNeAoaOlVAurIu",
    )

    # download visited urls json
    try:
        client.fget_object("group5", s3_folder+"visited_urls.json",
                           path_visited_urls)
    except Exception as e:
        if e.code == "NoSuchKey":
            # create file for visited urls if not existent
            with open(path_visited_urls, "w") as file:
                json.dump([], file)

    # load visited url list
    with open(path_visited_urls) as file:
        visited_urls = json.load(file)

    # reset list if too long (increases performance, duplicates unlikely)
    if len(visited_urls) > 100000:
        visited_urls = {}

    car_URLs = []

    # go through all of the 20 search pages looking for the car listings
    for page in range(1, 21):

        try:
            url = 'https://www.autoscout24.de/lst/?sort=age&desc=1&ustate=N%2CU&size=20&page=' + \
                str(page) + '&cy=D&atype=C&'
            only_a_tags = SoupStrainer("a")
            R = requests.get(url)
            soup = BeautifulSoup(R.content, 'lxml', parse_only=only_a_tags)
        except Exception as e:
            print("Übersicht: " + str(e) + " "*50, end="\r")
            pass

        else:
            # add every offer link inside the a tags to the car urls dict
            # IF they haven't been search already
            for link in soup.find_all("a"):
                if r"/angebote/" in str(link.get("href")):
                    car_link = str(link.get("href"))

                    if car_link not in visited_urls:
                        car_URLs.append(car_link)

            print(
                f'Seite {page} | {len(car_URLs)} neue URLs', end="\r")
    print("")

    return car_URLs

# function for parsing the autoscout24 json formatted listing details


def parseCarObject(car_obj):

    car_dict = {}

    try:
        carMileage = car_obj["props"]["pageProps"]["listingDetails"]["vehicle"]["mileageInKmRaw"]
        if carMileage > 0:
            car_dict["mileage"] = car_obj["props"]["pageProps"]["listingDetails"]["vehicle"]["mileageInKmRaw"]
        else:
            return None

        car_dict["make"] = car_obj["props"]["pageProps"]["listingDetails"]["vehicle"]["make"]
        car_dict["model"] = car_obj["props"]["pageProps"]["listingDetails"]["vehicle"]["model"]

        fuelCatDict = {
            "B": "Gasoline",
            "D": "Diesel",
            "E": "Electric",
            "2": "Electric/Gasoline",
            "3": "Electric/Diesel",
            "L": "LPG",
            "C": "CNG",
        }
        fuelCategory = car_obj["props"]["pageProps"]["listingDetails"]["vehicle"]["fuelCategory"]
        car_dict["fuel"] = fuelCatDict.get(
            fuelCategory["raw"], fuelCategory["formatted"])

        transmissionTypeDict = {
            "Schaltgetriebe": "Manual",
            "Automatik": "Automatic",
            "Halbautomatik": "Semi-automatic",
        }
        transmissionType = car_obj["props"]["pageProps"]["listingDetails"]["vehicle"]["transmissionType"]
        car_dict["gear"] = transmissionTypeDict.get(
            transmissionType, "")

        offerTypeDict = {
            "Jahreswagen": "Employee's car",
            "Oldtimer": "Oldtimer",
            "Vorführfahrzeug": "Demonstration",
            "Neu": "New",
            "Tageszulassung": "Pre-registered",
            "Gebraucht": "Used",
        }
        offerType = car_obj["props"]["pageProps"]["listingDetails"]["vehicle"]["legalCategories"][0]
        if offerType == "Neu":
            return None
        car_dict["offerType"] = offerTypeDict.get(
            offerType, "")

        car_dict["price"] = car_obj["props"]["pageProps"]["listingDetails"]["prices"]["public"]["priceRaw"]
        car_dict["hp"] = car_obj["props"]["pageProps"]["listingDetails"]["vehicle"]["rawPowerInHp"]

        dateRaw = car_obj["props"]["pageProps"]["listingDetails"]["vehicle"]["firstRegistrationDateRaw"]
        car_dict["year"] = datetime.strptime(
            dateRaw, '%Y-%m-%d').strftime('%Y')

    except Exception as e:
        print("Übersicht: " + str(e) + " "*50, end="\r")

    return car_dict


def scrapeList(car_URLs):

    global visited_urls
    multiple_cars_dict = {}
    car_counter = 1

    # visit every listing url and scrape for details
    for url in car_URLs:
        print(
            f'Auto {car_counter}'+' '*50, end="\r")

        car_counter += 1

        R = requests.get('https://www.autoscout24.de'+url)
        soup = BeautifulSoup(R.content, 'lxml')

        # load a24 json object containing all relevant info
        car_obj = json.loads(
            str((soup.find("script", {"id": "__NEXT_DATA__"}).text)))

        # create reduced dict from json object
        car_dict = parseCarObject(car_obj)

        if car_dict is not None:
            multiple_cars_dict[url] = car_dict
            visited_urls.append(url)

    print("")

    return multiple_cars_dict


def saveLists(multiple_cars_dict):

    global visited_urls
    set_header = False

    # create minio client
    client = Minio(
        "api.storage.sws.informatik.uni-leipzig.de",
        access_key="90iLSEUoCzGrPci8",
        secret_key="6scbjD5fbUSKuD1VULwNeAoaOlVAurIu",
    )

    # download car data from s3
    weekSubFolder = "week_"+datetime.today().strftime('%U')

    try:
        client.fget_object("group5", s3_folder+weekSubFolder+"/scraped_car_data.csv",
                           data_folder+"scraped_car_data.csv")
    except Exception as e:
        if e.code == "NoSuchKey":
            set_header = True

    if len(multiple_cars_dict) > 0:
        df = pd.DataFrame(multiple_cars_dict).T
        df.to_csv(data_folder+"scraped_car_data.csv", mode='a',
                  header=set_header, sep=";", index=False)
        client.fput_object(
            "group5", s3_folder+weekSubFolder +
            "/scraped_car_data.csv", data_folder+"scraped_car_data.csv",
        )
    else:
        print("Keine Daten")

    # save visited url list to S3
    with open(path_visited_urls, "w") as file:
        json.dump(visited_urls, file)

    client.fput_object(
        "group5", s3_folder+"visited_urls.json", path_visited_urls,
    )


if __name__ == "__main__":

    createStructure()

    list = createList()
    # sleep(5)

    if len(list) > 0:
        multiple_cars_dict = scrapeList(list)

        if len(multiple_cars_dict) > 0:
            saveLists(multiple_cars_dict)

    # print("\U0001F634")
    # sleep(300)
