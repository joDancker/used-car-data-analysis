"""Utility functions to extract car information from webpage."""
import re
from datetime import date, datetime, timedelta
from os.path import exists

import pandas as pd

from utils_website_scraping import scrape_webpage_for_car_characteristics


def initialize_or_import_dataset(path_to_existing_dataset, overwrite=True):
    """Extract car characteristics of advertisment from webpage.

    Parameters
    ----------
    path_to_existing_dataset : str
        path to file the which shall be imported
    overwrite : boolean
        file shall be overwritten

    Returns
    -------
    used_car_data : DataFrame
        used car data set
    """
    if exists(path_to_existing_dataset) and overwrite is True:
        print(f"Importing already existing file: {path_to_existing_dataset}")
        used_car_data = pd.read_csv(
            path_to_existing_dataset,
            dtype={
                "publication_history": str,
                "price_sek": int,
                "price_history": str,
                "entry_year": int,
                "mileage_km": int,
            },
            parse_dates=["publication_datetime"],
            infer_datetime_format="%Y-%m-%d %H:%M:%S",
        )
        used_car_data = used_car_data.iloc[:, 1:]
    else:
        print(f"Creating new dataset at: {path_to_existing_dataset}")
        used_car_data = pd.DataFrame(
            columns=[
                "publication_datetime",
                "publication_history",
                "location",
                "provider",
                "manufacturer",
                "model",
                "note",
                "price_sek",
                "price_history",
                "entry_year",
                "fuel",
                "mileage_km",
                "transmission",
                "type_of_drive",
                "horse_power",
                "engine_size_ccm",
                "top_speed_km_h",
                "emission_class",
                "co2_emission_g/km",
                "test_prozedure",
                "fuel_consumption_mixed_l_100km",
                "fuel_consumption_highway_l_100km",
                "electric_range_km",
                "number_of_seats",
                "car_type",
                "length_mm",
                "width_mm",
                "height_mm",
                "load_capacity_kg",
                "empty_weight_kg",
                "total_weight_kg",
                "url",
            ]
        )

    return used_car_data


def extract_car_characteristics(driver):
    """Extract car characteristics of advertisment from webpage.

    Parameters
    ----------
    driver : selenium.Webdriver
        webdriver for website interactions

    Returns
    -------
    car_characteristics : dict
        detailed characteristics of car advertisment
    """
    (
        publication_datetime,
        location,
        car_manufacturer_and_model,
        price,
        provider,
        key_characteristics,
        key_parameters,
        detailed_characteristics_and_parameters,
    ) = scrape_webpage_for_car_characteristics(driver)

    key_characteristics = [
        characteristic.text for characteristic in key_characteristics
    ]
    key_parameters = [parameter.text for parameter in key_parameters]
    car_characteristics = dict(zip(key_characteristics, key_parameters))

    car_characteristics["publication_datetime"] = extract_publication_datetime(
        publication_datetime
    )
    car_characteristics["location"] = extract_city(location)
    car_characteristics["price"] = extract_int_number(price)
    car_characteristics["provider"] = provider

    detailed_characteristics_and_parameters = [
        characteristic.text
        for characteristic in detailed_characteristics_and_parameters
    ]
    detailed_car_characteristics = convert_key_value_pair_list_to_dict(
        detailed_characteristics_and_parameters
    )
    car_characteristics.update(detailed_car_characteristics)

    manufacturer, model, note = extract_car_manufacturer_and_model(
        car_manufacturer_and_model
    )
    car_characteristics["manufacturer"] = manufacturer
    car_characteristics["note"] = note
    if car_characteristics.get("Modell") is None:
        car_characteristics["Modell"] = model

    return car_characteristics


def extract_publication_datetime(date_time):
    """Extract the datetime of publication.

    Parameters
    ----------
    date_time : str
        date and time of publication as scraped from webpage

    Returns
    -------
    date_time : datetime
        date and time of publication
    """
    datetime_parts = date_time.split()

    if any("idag" in string.lower() for string in datetime_parts):
        date_time = datetime_of_publication(date.today().weekday(), datetime_parts[-1])
    elif any("igår" in string.lower() for string in datetime_parts):
        date_time = datetime_of_publication(
            date.today().weekday() - 1, datetime_parts[-1]
        )
    elif any("måndag" in string.lower() for string in datetime_parts):
        date_time = datetime_of_publication(0, datetime_parts[-1])
    elif any("tisdag" in string.lower() for string in datetime_parts):
        date_time = datetime_of_publication(1, datetime_parts[-1])
    elif any("onsdag" in string.lower() for string in datetime_parts):
        date_time = datetime_of_publication(2, datetime_parts[-1])
    elif any("torsdag" in string.lower() for string in datetime_parts):
        date_time = datetime_of_publication(3, datetime_parts[-1])
    elif any("fredag" in string.lower() for string in datetime_parts):
        date_time = datetime_of_publication(4, datetime_parts[-1])
    elif any("lördag" in string.lower() for string in datetime_parts):
        date_time = datetime_of_publication(5, datetime_parts[-1])
    elif any("söndag" in string.lower() for string in datetime_parts):
        date_time = datetime_of_publication(6, datetime_parts[-1])
    elif "mars" in datetime_parts:
        datetime_parts[1] = "mar."
        date_time = datetime.strptime(" ".join(datetime_parts[1:]), "%d %b. %H:%M")
        date_time = date_time.replace(year=date.today().year)
    elif "maj" in datetime_parts:
        datetime_parts[1] = "may."
        date_time = datetime.strptime(" ".join(datetime_parts[1:]), "%d %b. %H:%M")
        date_time = date_time.replace(year=date.today().year)
    elif "juni" in datetime_parts:
        datetime_parts[1] = "jun."
        date_time = datetime.strptime(" ".join(datetime_parts[1:]), "%d %b. %H:%M")
        date_time = date_time.replace(year=date.today().year)
    elif "juli" in datetime_parts:
        datetime_parts[1] = "jul."
        date_time = datetime.strptime(" ".join(datetime_parts[1:]), "%d %b. %H:%M")
        date_time = date_time.replace(year=date.today().year)
    elif "okt." in datetime_parts:
        datetime_parts[1] = "oct."
        date_time = datetime.strptime(" ".join(datetime_parts[1:]), "%d %b. %H:%M")
        date_time = date_time.replace(year=date.today().year)
    else:
        date_time = datetime.strptime(" ".join(datetime_parts[1:]), "%d %b. %H:%M")
        date_time = date_time.replace(year=date.today().year)

    return date_time


def datetime_of_publication(weekday_of_publication, time_of_publication):
    """Derive the datetime of publication with respect to today's date.

    Parameters
    ----------
    weekday_of_publication : int
        day of the week ranging between 0 (monday) to 6 (sunday)
    time_of_publication : str
        time advertisment was published

    Returns
    -------
    date_time : datetime
        date and time of publication
    """
    days_between_publication_and_today = date.today().weekday() - weekday_of_publication

    # if weekday of publication lies before today the distance gets negative.
    # e.g weekday_of_publication is Sunday (6) and today is Wednesday (3)
    if days_between_publication_and_today < 0:
        days_between_publication_and_today = 7 + days_between_publication_and_today

    publication_date = date.today() - timedelta(days_between_publication_and_today)
    publication_date_time = " ".join(
        [publication_date.strftime("%Y-%m-%d"), time_of_publication]
    )
    publication_date_time = datetime.strptime(publication_date_time, "%Y-%m-%d %H:%M")

    return publication_date_time


def convert_datetime_to_str(date_time):
    """Convert datetime to string.

    Parameters
    ----------
    date_time : datetime
        date and time of publication

    Returns
    -------
    date_time : str
        date and time of publication
    """
    return datetime.strftime(date_time, format="%Y-%m-%d %H:%M:%S")


def extract_city(location):
    """Extract location of car.

    Location contains city and link to website showing the location on a map.

    Parameters
    ----------
    location : str
        location as scraped from webpage

    Returns
    -------
     : str
        only city as location
    """
    str_parts = location.split()
    return " ".join(str_parts[:-1])


def extract_car_manufacturer_and_model(ad_text):
    """Extract car manufacturer and model from advertisment header.

    Parameters
    ----------
    ad_text : str
        text of advertisment header

    Returns
    -------
    manufacturer : str
        car manufacturer
    model : str
        car model
    note : str
        additional notes given in advertisment header
    """
    str_parts = ad_text.split(maxsplit=2)
    manufacturer = str_parts[0]
    model = str_parts[1]
    if len(str_parts) > 2:
        note = str_parts[2]
    else:
        note = ""

    return manufacturer, model, note


def convert_key_value_pair_list_to_dict(characteristics_and_parameters):
    """Convert list of key value pairs to dict.

    Parameters
    ----------
    characteristics_and_parameters : list
        car characteristics and parameters

    Returns
    -------
     : dict
        car characteristics and parameters
    """
    return {
        "".join(characteristic.split("\n")[0:-1]): characteristic.split("\n")[-1]
        for characteristic in characteristics_and_parameters
    }


def convert_mileage(mileage):
    """Convert mileage as mileage is given in swedish miles.

    1 swedisch mile = 10 kilometers

    Parameters
    ----------
    mileage : str
        mileage of car in swedish miles

    Returns
    -------
    : int
        mileage of car  in kilometers
    """
    mileage = mileage.replace(" ", "")
    # sometimes given as a range; take larger value
    return int(mileage.split("-")[-1]) * 10


def attach_new_used_car(used_car_data, car_characteristics, url_car_advertisement):
    """Attach a new car to existing data set.

    Parameters
    ----------
    used_car_data : DataFrame
        data set of used cars
    car_characteristics : dict
        car characteristics which are to be appended to data set
    link_to_car_advertisement : str
        url of car advertisment

    Returns
    -------
    used_car_data : DataFrame
        updated data set of used cars
    """
    new_used_car = pd.DataFrame(
        [
            {
                "publication_datetime": car_characteristics["publication_datetime"],
                "location": car_characteristics["location"],
                "provider": car_characteristics["provider"],
                "manufacturer": car_characteristics["manufacturer"],
                "model": car_characteristics["Modell"],
                "note": car_characteristics["note"],
                "price_sek": car_characteristics["price"],
                "entry_year": car_characteristics.get("Modellår"),
                "fuel": translate_type_of_fuel(car_characteristics.get("Bränsle")),
                "mileage_km": convert_mileage(car_characteristics.get("Miltal")),
                "transmission": translate_type_of_transmission(
                    car_characteristics.get("Växellåda")
                ),
                "type_of_drive": translate_type_of_drive(
                    car_characteristics.get("Drivning")
                ),
                "horse_power": extract_int_number(
                    car_characteristics.get("Hästkrafter")
                ),
                "engine_size_ccm": extract_int_number(
                    car_characteristics.get("Motorstorlek")
                ),
                "top_speed_km_h": extract_int_number(
                    car_characteristics.get("Topphastighet")
                ),
                "emission_class": car_characteristics.get("Utsläppsklass"),
                "co2_emission_g/km": extract_int_number(
                    get_emissions(
                        car_characteristics.get("CO²-utsläpp (WLTP)"),
                        car_characteristics.get("CO²-utsläpp (NEDC)"),
                    )
                ),
                "test_prozedure": get_emissions_test_prozedure(
                    car_characteristics.get("CO²-utsläpp (WLTP)"),
                    car_characteristics.get("CO²-utsläpp (NEDC)"),
                ),
                "fuel_consumption_mixed_l_100km": extract_float_number(
                    car_characteristics.get("Bränsleförbrukning(vid blandad körning)")
                ),
                "fuel_consumption_highway_l_100km": extract_float_number(
                    car_characteristics.get("Bränsleförbrukning(vid landsväg)")
                ),
                "electric_range_km": extract_int_number(
                    car_characteristics.get("Elräckvidd (NECD)")
                ),
                "number_of_seats": car_characteristics.get("Antal säten"),
                "car_type": translate_type_of_car(car_characteristics.get("Biltyp")),
                "length_mm": extract_int_number(car_characteristics.get("Längd")),
                "width_mm": extract_int_number(car_characteristics.get("Bredd")),
                "height_mm": extract_int_number(car_characteristics.get("Höjd")),
                "load_capacity_kg": extract_int_number(
                    car_characteristics.get("Lastkapacitet")
                ),
                "empty_weight_kg": extract_int_number(
                    car_characteristics.get("Tjänstevikt (EU)")
                ),
                "total_weight_kg": extract_int_number(
                    car_characteristics.get("Totalvikt")
                ),
                "url": url_car_advertisement,
            }
        ]
    )

    used_car_data = pd.concat([used_car_data, new_used_car], axis=0, ignore_index=True)

    return used_car_data


def translate_type_of_transmission(transmission):
    """Translate transmission from swedish to english.

    Parameters
    ----------
    transmission : str
        type of transmission in swedish

    Returns
    -------
    : str
        type of transmission in english
    """
    if transmission == "Automat":
        return "automatic"
    elif transmission == "Manuell":
        return "manual"


def translate_type_of_drive(type_of_drive):
    """Translate type of drive from swedish to english.

    Parameters
    ----------
    type_of_drive : str
        type of type of drive in swedish

    Returns
    -------
    : str
        type of type of drive in english
    """
    if type_of_drive == "Fyrhjulsdrift" or type_of_drive == "Fyrhjulsdriven":
        return "four-wheel drive"
    elif type_of_drive == "Tvåhjulsdrift" or type_of_drive == "Tvåhjulsdriven":
        return "two-wheel drive"
    else:
        return type_of_drive


def translate_type_of_car(type_of_car):
    """Translate type of car from swedish to english.

    Parameters
    ----------
    type_of_car : str
        type of type of car in swedish

    Returns
    -------
    : str
        type of type of car in english
    """
    if type_of_car == "Kombi":
        return "estate car"
    elif type_of_car == "Halvkombi":
        return "hatchback"
    elif type_of_car == "Småbil":
        return "small"
    elif type_of_car == "Cap":
        return "convertible"
    elif type_of_car == "Familjebuss":
        return "van"
    elif type_of_car == "Yrkesfordon":
        return "commercial"
    else:
        return type_of_car


def translate_type_of_fuel(fuel):
    """Translate type of fuel from swedish to english.

    Parameters
    ----------
    fuel : str
        type of type of fuel in swedish

    Returns
    -------
    : str
        type of type of fuel in english
    """
    if fuel == "Diesel":
        return "diesel"
    elif fuel == "Bensin":
        return "petrol"
    elif fuel == "Miljöbränsle/Hybrid":
        return "hybrid"
    elif fuel == "El":
        return "electric"


def extract_int_number(string):
    """Extract integer number from string.

    Parameters
    ----------
    string : str
        number as string

    Returns
    -------
    : int
        number as integer
    """
    if string is not None:
        num = "".join(re.findall(r"\d+", string))
        if num != "":
            return int(num)
        else:
            return None
    else:
        return None


def extract_float_number(string):
    """Extract float number from string.

    Parameters
    ----------
    string : str
        number as string

    Returns
    -------
    : float
        number as float
    """
    if string is not None:
        return float(string.split()[0])
    else:
        return None


def get_emissions(WLTP, NEDC):
    """Extract float number from string.

    Parameters
    ----------
    WLTP : str
        CO2 emissions of WLTP test procedure
    NEDC : str
        CO2 emissions of NEDC test procedure

    Returns
    -------
    : str
        CO2 emissions
    """
    if WLTP is not None:
        return WLTP
    else:
        return NEDC


def get_emissions_test_prozedure(WLTP, NEDC):
    """Extract float number from string.

    Parameters
    ----------
    WLTP : str
        CO2 emissions of WLTP test procedure
    NEDC : str
        CO2 emissions of NEDC test procedure

    Returns
    -------
    : str
        emission's test procedure
    """
    if WLTP is not None:
        return "WLTP"
    elif NEDC is not None:
        return "NEDC"
    else:
        return None
