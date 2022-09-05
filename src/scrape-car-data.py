"""Scrape used car data."""
from selenium import webdriver

from utils_car_characteristic_extraction import (
    attach_new_used_car,
    extract_car_characteristics,
    initialize_or_import_dataset,
)
from utils_update_advertisment import (
    car_is_uploaded_again,
    update_price_of_car,
    update_publication_datetime_of_car,
)
from utils_website_interaction import (
    accept_cookies,
    close_information_banner_and_pop_ups,
    expand_detailed_car_information_arcordeon,
    go_to_next_webpage_with_results,
    open_webpage,
)
from utils_website_scraping import (
    scrape_links_to_detailed_car_advertisement,
    scrape_number_of_result_webpages,
)

start_webpage = 1
urlpage = "url_of_website"

path_to_dataset = "data/used_car_dataset.csv"
overwrite = True

used_car_data = initialize_or_import_dataset(path_to_dataset, overwrite)


print("opening firefox.")
driver_search_result_overview = webdriver.Firefox()
driver_detailed_car_result = webdriver.Firefox()

print("opening webpage.")
open_webpage(driver_search_result_overview, urlpage)
accept_cookies(driver_search_result_overview)
close_information_banner_and_pop_ups(driver_search_result_overview)

number_of_result_webpages = scrape_number_of_result_webpages(
    driver_search_result_overview
)

for result_webpage in range(number_of_result_webpages):
    number_existing_cars_in_data = 0

    print(f"scraping webpage {start_webpage+result_webpage}.")

    all_links_to_car_advertisements = scrape_links_to_detailed_car_advertisement(
        driver_search_result_overview
    )

    for link_to_car_advertisement in all_links_to_car_advertisements:

        open_webpage(driver_detailed_car_result, link_to_car_advertisement)
        accept_cookies(driver_detailed_car_result)
        close_information_banner_and_pop_ups(driver_detailed_car_result)

        car_exists_idx = used_car_data.index[
            used_car_data["url"].eq(link_to_car_advertisement)
        ]
        if len(car_exists_idx):

            if car_is_uploaded_again(
                used_car_data.loc[car_exists_idx], driver_detailed_car_result
            ):

                used_car_data.loc[car_exists_idx] = update_publication_datetime_of_car(
                    used_car_data.loc[car_exists_idx], driver_detailed_car_result
                )

                used_car_data.loc[car_exists_idx] = update_price_of_car(
                    used_car_data.loc[car_exists_idx], driver_detailed_car_result
                )

                continue

            else:
                number_existing_cars_in_data = number_existing_cars_in_data + 1
                print(
                    f"{number_existing_cars_in_data} car(s) already exist in data set."
                )
                continue

        expand_detailed_car_information_arcordeon(driver_detailed_car_result)

        try:
            car_characteristics = extract_car_characteristics(
                driver_detailed_car_result
            )
        except Exception:
            continue

        used_car_data = attach_new_used_car(
            used_car_data, car_characteristics, link_to_car_advertisement
        )

    if overwrite:
        print("saving dataset.")
        used_car_data.to_csv(path_to_dataset)

    go_to_next_webpage_with_results(driver_search_result_overview)


print("closing firefox.")
driver_search_result_overview.quit()
driver_detailed_car_result.quit()
