import requests
from bs4 import BeautifulSoup
import csv


def get_td_text(row, class_name):
    td = row.find('td', class_=class_name)
    return td.text.strip() if td else ""

csv_filename = "toxicity_data.csv"
with open(csv_filename, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    table_header = ["Animal Name", "Chemical", "Endpoint Value", "Endpoint Description", "Range", "Sex", "Life Cycle Stage", "Location", "Sample Size", "Tox Exposure", "Toxicity Endpoint Type", "Tox Exposure Duration", "Tox Exposure Technique", "Type"]
    writer.writerow(table_header)
    for page_num in range(107):
        print("\n")
        print("Page Num: ", page_num)
        url =f"https://ecotox.oehha.ca.gov/explore?type=ecotox_toxicity_dataset&page={page_num}"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        view_groupings = soup.find_all("div", class_="view-grouping")
        rows_len = 0
        for idx, group in enumerate(view_groupings, start=1):
            #Find the name of the animal
            header = group.find("div", class_="view-grouping-header")
            a_tag = header.find("a")
            if a_tag:
                a_text = a_tag.get_text(strip=True)
            else:
                a_text = ""

            content = group.find("div", class_="view-grouping-content")
            tables = content.find_all("table")
            for table in tables:
                rows = table.find_all("tr")[1:]
                for row in rows:
                    chemical_td = get_td_text(row, 'views-field-field-ecotox-chemical-1')
                    endpoint_value_td = get_td_text(row, 'views-field-field-ecotox-endpt-value')
                    endpoint_description_td = get_td_text(row, 'views-field-field-ecotox-endpt-description')
                    range_td = get_td_text(row, 'views-field-field-ecotox-range')
                    sex_td = get_td_text(row, 'views-field-field-ecotox-sex')
                    life_cycle_stage_td = get_td_text(row, 'views-field-field-ecotox-life-stage')
                    location_td = get_td_text(row, 'views-field-field-ecotox-specific-location')
                    sample_size_td = get_td_text(row, 'views-field-field-ecotox-sample-size')
                    tox_exposure_td = get_td_text(row, 'views-field-field-ecotox-tox-exposure')
                    tox_endopoint_type_td = get_td_text(row, 'views-field-field-ecotox-toxicity-endpt')
                    tox_exposure_dur_td = get_td_text(row, 'views-field-field-ecotox-tox-exp-duration')
                    tox_exposure_tech_td = get_td_text(row, 'views-field-field-ecotox-tox-exp-technique')
                    type_td = get_td_text(row, 'views-field-type')

                    row_data = [
                        a_text, 
                        chemical_td, 
                        endpoint_value_td, 
                        endpoint_description_td,
                        range_td,
                        sex_td,
                        life_cycle_stage_td,
                        location_td,
                        sample_size_td,
                        tox_exposure_td,
                        tox_endopoint_type_td,
                        tox_exposure_dur_td,
                        tox_exposure_tech_td,
                        type_td
                    ]
                    writer.writerow(row_data)
