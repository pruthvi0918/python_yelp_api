""" PyYelpAPI module reads data from Yelp business API and insert data to sqlite3 database"""
import requests
import sqlite3
from pathlib import Path
import os
import configparser
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)


class PyYelpAPI:

    def get_yelp_api_restaurant_data(self):
        """ Reads data from Yelp business endpoint for all Restaurant in BOS location"""
        thisfolder = os.path.dirname(os.path.abspath(__file__))
        initfile = os.path.join(thisfolder, r'configuration.txt')
        logging.info(logging.getLoggerClass().root.handlers[0].baseFilename)
        logging.info(f"Current folder : {thisfolder}")
        config = configparser.ConfigParser()
        config.read(initfile)
        url = config.get('YELP-API-INFO', 'url')
        api_key = config.get('YELP-API-INFO', 'api_key')
        logging.info(url)
        logging.info(api_key)

        headers_dict = {
            "Authorization": "Bearer "+api_key
        }
        params_dict = {
            "term": "Restaurant",
            "location": "BOS"
        }
        return requests.get(url, headers=headers_dict, params=params_dict)

    def insert_api_data_to_table(self, response):
        """ insert data into Resturant table by reading YELP API JSON response """
        try:
            businesses_list = response.json()["businesses"]
            with sqlite3.connect("db.sqllite3") as connection_ref:
                command = "INSERT INTO RESTAURANT VALUES (?, ? , ?)"

                for each_business_item in businesses_list:
                    name = each_business_item["name"]
                    review_count = each_business_item["review_count"]
                    phone = each_business_item["phone"]
                    logging.info(
                        f"Data inserted into RESTAURANT table is: {name} , {review_count}, {phone}")

                    data = (name, review_count, phone)
                    connection_ref.execute(command, data)
                    connection_ref.commit()
                return True
        except Exception as ex:
            logging.error("Something went wrong during data insertion")
            logging.error(ex)
            return False


response = PyYelpAPI().get_yelp_api_restaurant_data()
PyYelpAPI().insert_api_data_to_table(response)
