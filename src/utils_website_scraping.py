"""Utility functions for scraping elements on webpage."""

from selenium.webdriver.common.by import By


def scrape_information_banner_close_button(driver):
    """Scrape close button of information banner.

    Parameters
    ----------
    driver : selenium.Webdriver
        webdriver for website interactions

    Returns
    -------
    : selenium.WebElement
        webelement with extracted information
    """
    return driver.find_element(
        By.CSS_SELECTOR, "button[class='IconButton__Button-slrzzc-2 XmByt']"
    )


def scrape_pop_up_close_button(driver):
    """Scrape close button of pop up windows.

    Parameters
    ----------
    driver : selenium.Webdriver
        webdriver for website interactions

    Returns
    -------
    : selenium.WebElement
        webelement with extracted information
    """
    return driver.find_element(By.CSS_SELECTOR, "button[class='sg-b-p-c']")


def scrape_cookie_accept_button(driver):
    """Scrape accept button of cookie window.

    Parameters
    ----------
    driver : selenium.Webdriver
        webdriver for website interactions

    Returns
    -------
    : selenium.WebElement
        webelement with extracted information
    """
    return driver.find_element(by=By.ID, value="accept-ufti")


def scrape_detail_arcordeon_expansion_buttons(driver):
    """Scrape expansion buttons of accoredon with detailed car information.

    Parameters
    ----------
    driver : selenium.Webdriver
        webdriver for website interactions

    Returns
    -------
    : selenium.WebElement
        webelement with extracted information
    """
    return driver.find_elements(
        By.CSS_SELECTOR,
        "div[class='TextCallout2__TextCallout2Wrapper-sc-1bir8f0-0 dVkfPB Transportstyrelsen__AccordionTitle-sc-6tq5gz-3 hSRAnA']",  # noqa
    )


def scrape_change_result_webpage_button(driver):
    """Scrape buttons for changing between result webpages.

    Parameters
    ----------
    driver : selenium.Webdriver
        webdriver for website interactions

    Returns
    -------
    : list
        selenium.WebElements with extracted information
    """
    return driver.find_elements(
        By.CSS_SELECTOR,
        "a[class='Pagination__Button-sc-uamu6s-1 Pagination__PrevNextButton-sc-uamu6s-7 gHhaEf bXvjTf']",  # noqa
    )


def scrape_links_to_detailed_car_advertisement(driver):
    """Scrape links to webpages of car advertisments with detailed car information.

    Parameters
    ----------
    driver : selenium.Webdriver
        webdriver for website interactions

    Returns
    -------
    : list
        selenium.WebElements with extracted information
    """
    all_links_to_details = scrape_links_to_car_advertisment(driver)
    all_providers = scrape_all_providers(driver)

    # sometimes there is an ad banner above the actual list of cars, which has the same
    # CSS-tags that are read above. These cars in the banner, however, have a different
    # set of information that leads to issues in the actual scarping process. Therefore,
    # the cars in the banner are not included in the scraping.
    # It seems as the number of providers extracted equals the number of cars in the
    # list (seems like the banner does not include the CSS-tag which is used to extract
    # the car providers). Based on that number the other scraped datasets are reduced
    # counting from their end until.
    number_of_cars_on_page = len(all_providers)
    if number_of_cars_on_page > 40:
        number_of_cars_on_page = 40

    return all_links_to_details[-number_of_cars_on_page:]


def scrape_webpage_for_car_characteristics(driver):
    """Scrape webpage for detailed car characteristics.

    Parameters
    ----------
    driver : selenium.Webdriver
        webdriver for website interactions

    Returns
    -------
    publication_datetime : str
        datetime the advertisment was published
    location : str
        city the car is located
    car_manufacturer_and_model : str
        manufacturer and model of car
    price : str
        price of car
    provider : str
        provider that published the advertisment
    general_characteristics : str
        overview of general car characteristics
    general_parameters : str
        overview of general car parameters
    detailed_characteristics_and_parameters : str
        detailed car characteristics and parameters
    """
    publication_datetime = scrape_publication_datetime(driver)
    location = scrape_location(driver)
    car_manufacturer_and_model = scrape_car_manufacturer_and_model(driver)
    price = scrape_price_of_car(driver)
    provider = scrape_provider(driver)
    general_characteristics = scrape_general_car_characteristic_keys(driver)
    general_parameters = scrape_general_car_characteristic_parameters(driver)
    detailed_characteristics_and_parameters = (
        scrape_detailed_car_characteristic_keys_and_parameters(driver)
    )

    return (
        publication_datetime,
        location,
        car_manufacturer_and_model,
        price,
        provider,
        general_characteristics,
        general_parameters,
        detailed_characteristics_and_parameters,
    )


def scrape_publication_datetime(driver):
    """Scrape datetime of advertisement's publication.

    Parameters
    ----------
    driver : selenium.Webdriver
        webdriver for website interactions

    Returns
    -------
    : str
        extracted information
    """
    return driver.find_element(
        By.CSS_SELECTOR,
        "span[class='TextCallout2__TextCallout2Wrapper-sc-1bir8f0-0 dVkfPB PublishedTime__StyledTime-sc-pjprkp-1 gaxNzF']",  # noqa
    ).text


def scrape_location(driver):
    """Scrape location of car.

    Parameters
    ----------
    driver : selenium.Webdriver
        webdriver for website interactions

    Returns
    -------
    : str
        extracted information
    """
    try:
        return driver.find_element(
            By.CSS_SELECTOR,
            "a[class='Link-sc-6wulv7-0 LocationInfo__StyledMapLink-sc-1op511s-3 kVcpUt bEePwY']",  # noqa
        ).text
    except Exception:
        # sometimes no location is given as car is provided by online provider
        return "online"


def scrape_car_manufacturer_and_model(driver):
    """Scrape car manufacturer and model.

    Parameters
    ----------
    driver : selenium.Webdriver
        webdriver for website interactions

    Returns
    -------
    : selenium.WebElement
        webelement with extracted information
    """
    return driver.find_element(
        By.CSS_SELECTOR,
        "h1[class='TextHeadline1__TextHeadline1Wrapper-sc-1bi3cli-0 bIxKdL Hero__StyledSubject-sc-1mjgwl-4 dGnKKn']",  # noqa
    ).text


def scrape_price_of_car(driver):
    """Scrape price of car.

    Parameters
    ----------
    driver : selenium.Webdriver
        webdriver for website interactions

    Returns
    -------
    : str
        extracted information
    """
    try:
        price = driver.find_element(
            By.CSS_SELECTOR,
            "div[class='TextHeadline1__TextHeadline1Wrapper-sc-1bi3cli-0 bIxKdL Price__StyledPrice-sc-crp2x0-0 kIhjJa']",  # noqa
        ).text
    except Exception:
        # sometimes no price is given with car
        price = ""

    return price


def scrape_provider(driver):
    """Scrape provider of car.

    Parameters
    ----------
    driver : selenium.Webdriver
        webdriver for website interactions

    Returns
    -------
    : str
        extracted information
    """
    return driver.find_element(
        By.CSS_SELECTOR,
        "div[class='TextSubHeading__TextSubHeadingWrapper-sc-1c6hp2-0 gQCEZy styled__AdvertiserName-sc-1f8y0be-7 wJamH']",  # noqa
    ).text


def scrape_general_car_characteristic_keys(driver):
    """Scrape keys of general car characteristics.

    This includes mileage, type of fuel, transmission, entry year of car,
    type of car, type of drive

    Parameters
    ----------
    driver : selenium.Webdriver
        webdriver for website interactions

    Returns
    -------
    : list
        selenium.WebElements with extracted information
    """
    elements = driver.find_elements(
        By.CSS_SELECTOR,
        "div[class='TextCallout2__TextCallout2Wrapper-sc-1bir8f0-0 dVkfPB ParamsWithIcons__StyledLabel-sc-hanfos-2 eSsBiw']",  # noqa
    )

    return [element.text for element in elements]


def scrape_general_car_characteristic_parameters(driver):
    """Scrape parameters of general car characteristics.

    Parameters
    ----------
    driver : selenium.Webdriver
        webdriver for website interactions

    Returns
    -------
    : list
        selenium.WebElements with extracted information
    """
    elements = driver.find_elements(
        By.CSS_SELECTOR,
        "div[class='TextCallout1__TextCallout1Wrapper-swd73-0 juCWPZ ParamsWithIcons__StyledParamValue-sc-hanfos-3 kvNStP']",  # noqa
    )

    return [element.text for element in elements]


def scrape_detailed_car_characteristic_keys_and_parameters(driver):
    """Scrape detailed car characteristics and parameters.

    This includes CO2 emissions, fuel consumption, size of car, etc.

    Parameters
    ----------
    driver : selenium.Webdriver
        webdriver for website interactions

    Returns
    -------
    : list
        extracted information
    """
    elements = driver.find_elements(
        By.CSS_SELECTOR,
        "div[class='TextCallout2__TextCallout2Wrapper-sc-1bir8f0-0 dVkfPB Transportstyrelsen__AccordionContentRow-sc-6tq5gz-4 bxCoHS']",  # noqa
    )

    return [element.text for element in elements]


def scrape_links_to_car_advertisment(driver):
    """Scrape links to webpages with car advertisments.

    # the clas-tags may be different from time to time. Hence, check different tags.

    Parameters
    ----------
    driver : selenium.Webdriver
        webdriver for website interactions

    Returns
    -------
    : list
        selenium.WebElements with extracted information
    """
    all_links_to_details = driver.find_elements(
        By.CSS_SELECTOR,
        "a[class='Link-sc-6wulv7-0 styled__StyledTitleLink-sc-1kpvi4z-11 kVcpUt kbgaQK']",  # noqa
    )

    if not all_links_to_details:
        all_links_to_details = driver.find_elements(
            By.CSS_SELECTOR,
            "a[class='Link-sc-6wulv7-0 styled__StyledTitleLink-sc-1kpvi4z-11 kVcpUt gNDIDM']",  # noqa
        )

    if not all_links_to_details:
        all_links_to_details = driver.find_elements(
            By.CSS_SELECTOR,
            "a[class='Link-sc-6wulv7-0 styled__StyledTitleLink-sc-1kpvi4z-11 kVcpUt iqASGc']",  # noqa
        )

    return [link.get_attribute("href") for link in all_links_to_details]


def scrape_all_providers(driver):
    """Scrape all providers on webpage.

    Parameters
    ----------
    driver : selenium.Webdriver
        webdriver for website interactions

    Returns
    -------
    : list
        selenium.WebElements with extracted information
    """
    return driver.find_elements(
        By.CSS_SELECTOR,
        "div[class='TextCallout2__TextCallout2Wrapper-sc-1bir8f0-0 dVkfPB StoreInfo__StoreName-sc-t7web5-0 eAWtEJ']",  # noqa
    )


def scrape_number_of_result_webpages(driver):
    """Scrape number of result webpages with car advertisments.

    Parameters
    ----------
    driver : selenium.Webdriver
        webdriver for website interactions

    Returns
    -------
    : int
        number of result webpages
    """
    total_number = driver.find_elements(
        By.CSS_SELECTOR, "a[class='Pagination__Button-sc-uamu6s-1 gHhaEf']"
    )[-1].text

    return int(total_number)
