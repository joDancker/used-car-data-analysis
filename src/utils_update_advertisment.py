"""Utility functions for updating a car advertisment that's already in the dataset."""
from utils_car_characteristic_extraction import (
    convert_datetime_to_str,
    extract_int_number,
    extract_publication_datetime,
)
from utils_website_scraping import scrape_price_of_car, scrape_publication_datetime


def update_car_history(history_of_car, old_value):
    """Update car history in data set.

    This can be either the publication datetime or the price of the car.

    Parameters
    ----------
    history_of_car : pd.Series
        history of car advertisment
    old_value : str or int
        old value of car

    Returns
    -------
    history_of_car : str
        updated history of car advertisment
    """
    if history_of_car.isna().values:
        history_of_car = str(old_value)
    else:
        history_of_car = str(old_value) + ", " + str(history_of_car)

    return history_of_car


def car_is_uploaded_again(advertisment, driver):
    """Check if advertisment already exists in dataset and is updated.

    Parameters
    ----------
    advertisment : pd.Series
        data of car
    driver : str or int
        selenium.WebElement of webpage with car details

    Returns
    -------
     : bolean
        updated history of car advertisment
    """
    (
        new_publication_date_time,
        old_publication_date_time,
        publication_date_time_history,
    ) = get_advertisment_datetimes(advertisment, driver)

    return (new_publication_date_time not in old_publication_date_time) and (
        new_publication_date_time not in publication_date_time_history
    )


def update_publication_datetime_of_car(advertisment, driver):
    """Update the publication date and history of car.

    Parameters
    ----------
    advertisment : pd.Series
        data of car
    driver : str or int
        selenium.WebElement of webpage with car details

    Returns
    -------
    advertisment : pd.Series
        updated data of car
    """
    (
        new_publication_date_time,
        old_publication_date_time,
        publication_date_time_history,
    ) = get_advertisment_datetimes(advertisment, driver)

    print(
        f"Car advertisment from {old_publication_date_time} has been uploaded again on",
        f"{new_publication_date_time}.",
    )

    advertisment["publication_datetime"] = new_publication_date_time
    advertisment["publication_history"] = update_car_history(
        publication_date_time_history,
        old_publication_date_time,
    )

    return advertisment


def get_advertisment_datetimes(advertisment, driver):
    """Update the publication datetime and history of car.

    Parameters
    ----------
    advertisment : pd.Series
        data of car
    driver : str or int
        selenium.WebElement of webpage with car details

    Returns
    -------
    new_publication_date_time : str
        new publication datetime
    old_publication_date_time : str
        old publication datetime
    publication_date_time_history : str
        history of publication datetimes
    """
    new_publication_date_time = convert_datetime_to_str(
        extract_publication_datetime(scrape_publication_datetime(driver))
    )
    old_publication_date_time = convert_datetime_to_str(
        advertisment["publication_datetime"].item()
    )
    publication_date_time_history = advertisment["publication_history"]

    return (
        new_publication_date_time,
        old_publication_date_time,
        publication_date_time_history,
    )


def update_price_of_car(advertisment, driver):
    """Update the price and history of car.

    Parameters
    ----------
    advertisment : series
        data of car
    driver : object
        selenium.WebElement of webpage with car details

    Returns
    -------
    advertisment : series
        updated data of car
    """
    new_car_price = extract_int_number(scrape_price_of_car(driver))
    old_car_price = advertisment["price_sek"].item()
    car_price_history = advertisment["price_history"]

    print(f"Price of car has changed from {old_car_price} to {new_car_price}.")

    advertisment["price_sek"] = new_car_price
    advertisment["price_history"] = update_car_history(
        car_price_history,
        old_car_price,
    )

    return advertisment
