"""Utility functions for website interaction, such as clicking buttons."""

from utils_website_scraping import (
    scrape_change_result_webpage_button,
    scrape_cookie_accept_button,
    scrape_detail_arcordeon_expansion_buttons,
    scrape_information_banner_close_button,
    scrape_pop_up_close_button,
)


def open_webpage(driver, urlpage):
    """Open webpage.

    Parameters
    ----------
    driver : selenium.Webdriver
        webdriver for website interactions
    urlpage : str
        url of webpage to be opened
    """
    driver.get(urlpage)
    driver.implicitly_wait(0.5)


def accept_cookies(driver):
    """Accept Cookies when cookie window is available.

    Parameters
    ----------
    driver : selenium.Webdriver
        webdriver for website interactions
    """
    try:
        scrape_cookie_accept_button(driver).click()
    except Exception:
        pass


def close_information_banner_and_pop_ups(driver):
    """Close information banner or pop ups that might appear when opening a webpage.

    Parameters
    ----------
    driver : selenium.Webdriver
        webdriver for website interactions
    """
    try:
        scrape_information_banner_close_button(driver).click()
    except Exception:
        pass

    try:
        scrape_pop_up_close_button(driver).click()
    except Exception:
        pass


def expand_detailed_car_information_arcordeon(driver):
    """Expand the acccordeon containing the detailed car information.

    Parameters
    ----------
    driver : selenium.Webdriver
        webdriver for website interactions
    """
    for button in scrape_detail_arcordeon_expansion_buttons(driver):
        try:
            button.click()
        except Exception:
            pass


def go_to_next_webpage_with_results(driver):
    """Go to next webpage containing more car advertisments.

    Parameters
    ----------
    driver : selenium.Webdriver
        webdriver for website interactions
    """
    # as there is a backward and forward button choose last, which corresponds to
    # forward button
    scrape_change_result_webpage_button(driver)[-1].click()
    driver.implicitly_wait(3)
