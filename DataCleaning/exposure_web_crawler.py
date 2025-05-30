import requests
from bs4 import BeautifulSoup
import csv


def get_td_text(row, class_name):
    td = row.find('td', class_=class_name)
    return td.text.strip() if td else ""

csv_filename = "exposure_data.csv"
num_rows = 1
with open(csv_filename, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    table_header = ["Animal Name", "Exposure Endpoint Type", "Endpoint Value", "Endpoint Description", "Range", "Units", "Error", "Sex", "Life Cycle Stage", "Location", "Sample Size", "Type"]
    writer.writerow(table_header)
    for page_num in range(130):
        print("\n")
        print("Page Num: ", page_num)
        url =f"https://ecotox.oehha.ca.gov/explore?type=ecotox_exposure_dataset&page={page_num}"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        view_groupings = soup.find_all("div", class_="view-grouping")
        for idx, group in enumerate(view_groupings, start=1):
            #Find the name of the animal
            header = group.find("div", class_="view-grouping-header")
            a_tag = header.find("a")
            if a_tag:
                a_text = a_tag.get_text(strip=True)
            else:
                a_text = ""

            print(f"\tAnimal Name: {a_text}")
            print(f"\t\trow {num_rows+1}-", end="")

            content = group.find("div", class_="view-grouping-content")
            tables = content.find_all("table")
            for table in tables:
                rows = table.find_all("tr")[1:]
                for row in rows:
                    endpoint_type_td = get_td_text(row, 'views-field-field-ecotox-exposure-endpt')
                    endpoint_value_td = get_td_text(row, 'views-field-field-ecotox-endpoint-value')
                    endpoint_description_td = get_td_text(row, 'views-field-field-ecotox-endpt-description')
                    range_td = get_td_text(row, 'views-field-field-ecotox-range')
                    units_td = get_td_text(row, 'view-field-ecotox-units-table-column')
                    error_td = get_td_text(row, 'views-field-field-ecotox-error')
                    sex_td = get_td_text(row, 'views-field-field-ecotox-sex')
                    life_cycle_stage_td = get_td_text(row, 'views-field-field-ecotox-life-stage')
                    location_td = get_td_text(row, 'views-field-field-ecotox-specific-location')
                    sample_size_td = get_td_text(row, 'views-field-field-ecotox-sample-size')
                    type_td = get_td_text(row, 'views-field-type')

                    row_data = [
                        a_text, 
                        endpoint_type_td,
                        endpoint_value_td, 
                        endpoint_description_td,
                        range_td,
                        units_td,
                        error_td,
                        sex_td,
                        life_cycle_stage_td,
                        location_td,
                        sample_size_td,
                        type_td
                    ]
                    writer.writerow(row_data)
                    num_rows += 1
            print(f"{num_rows}")
